import numpy as np

from exibicao import (
    concatenar_representacoes,
    colorir_celula,
    gerar_cabecalho_matriz
)
from utils import cima, baixo, direita, esquerda
from algoritmos import algoritmo_bfs, zigue_zague
from constantes import (
    PISO_LIMPO,
    OBSTACULO,
    PISO_SUJO,
    NAO_EXPLORADO,
    BATERIA_BAIXA,
    BATERIA_POUCO_GASTA,
    LIMPEZAS_NECESSARIAS_PARA_ENCERRAR_EXPLORACAO
)


class Aspirador:
    linha = 0
    coluna = 0
    acoes = ["cima", "baixo", "esquerda", "direita", "aspirar", "recarregar"]
    direcao = "baixo" # Diz se o robo está subindo ou descendo no zig zague
    ultima_movimentacao_executada = ""
    rota_desvio = [] # quais coordenadas devem ser percorridas para o aspirador se deslocar para uma determinada célula
    desviando = False
    descarregando = False
    capacidade_bateria = 0
    limpezas_efetuadas = 0
    modo_operacao = "exploração"
    executando_rota_limpeza = False

    def __init__(self, bateria, linhas, colunas):
        self.capacidade_bateria = bateria
        self.bateria = bateria
        self.modelo_interno = np.zeros((linhas, colunas), int)
        self.modelo_interno.fill(NAO_EXPLORADO)
        self.contadores = np.zeros((linhas, colunas), int)
        self.posicao_carregador = ()
        self.possiveis_hotspots = []
        self.rota_limpeza = []
        self.ultima_posicao = (0,0)


    def atualiza_modelo_interno(self, percepcao):
        """Atualiza o modelo interno do ambiente que o agente possui"""
        if percepcao["cima"] == OBSTACULO:
            self.modelo_interno[self.linha - 1][self.coluna] = percepcao["cima"]

        if percepcao["direita"] == OBSTACULO:
            self.modelo_interno[self.linha][self.coluna + 1] = percepcao["direita"]

        if percepcao["baixo"] == OBSTACULO:
            self.modelo_interno[self.linha + 1][self.coluna] = percepcao["baixo"] 

        if percepcao["esquerda"] == OBSTACULO:
            self.modelo_interno[self.linha][self.coluna - 1] = percepcao["esquerda"]

        self.modelo_interno[self.linha][self.coluna] = percepcao["atual"]

    def program(self, percepcao):
        """Retorna a próxima ação do agente com nas suas percepções
        e no seu estado atual"""

        if self.modo_operacao == "limpeza":
            if self.executando_rota_limpeza:
                self.rota_limpeza = self.calcular_rota_limpeza()
                self.rota_desvio = self.bfs(self.get_posicao(), self.posicao_carregador) + self.rota_limpeza
                self.executando_rota_limpeza = False
                        
        self.atualiza_modelo_interno(percepcao)

        # Faz mudar o modo de operação
        if self.limpezas_efetuadas >= LIMPEZAS_NECESSARIAS_PARA_ENCERRAR_EXPLORACAO and self.modo_operacao == "exploração":
            self.modo_operacao = "limpeza"
            self.possiveis_hotspots = self.calcular_possiveis_hotspots()
            self.rota_limpeza = self.calcular_rota_limpeza()
            
            print("self.possiveis_hotspots", self.possiveis_hotspots)
            print("self.rota_limpeza:", self.rota_limpeza)
            self.rota_desvio = self.bfs(self.get_posicao(), self.posicao_carregador) + self.rota_limpeza

        # Recarrega, a menos que esteja com uma bateria muito cheia
        if self.posicao_carregador == self.get_posicao() and self.get_bateria() <= BATERIA_POUCO_GASTA:
            return "recarregar"

        # Limpa o piso, se não tiver com bateria muito baixa 
        if percepcao["atual"] == PISO_SUJO and not self.descarregando:
            return "limpar"

        # Parar zigue-zague e ir direto para o carregador
        if self.get_bateria() <= BATERIA_BAIXA and not self.descarregando:
            self.ultima_posicao = self.get_posicao()
            print("self.ultima_posicao:", self.ultima_posicao)
            self.descarregando = True
            self.desviando = True
            self.rota_desvio = self.bfs(self.get_posicao(), self.posicao_carregador)
            movimento = self.desviar() # executa o primeiro movimento do desvio
            return movimento

        # Fazer desvio para retornar ao zigue-zague, depois de ter carregado
        if self.get_bateria() > BATERIA_POUCO_GASTA and self.descarregando:
            print("retornando ao zigue-zague")
            self.desviando = True
            self.descarregando = False
            self.rota_desvio = self.bfs(self.get_posicao(), self.ultima_posicao)
            movimento = self.desviar() # executa o primeiro movimento do desvio
            return movimento

        # Executa movimentação normal
        if self.rota_desvio == []:
            movimento = self.zigue_zague()
            self.desviando = False

            # Se for colidir, calcular desvio
            if self.checar_colisao_obstaculos(movimento):
                tipo_desvio = self.calcula_tipo_desvio(movimento)
                destino = self.calcula_destino(self.linha, self.coluna, movimento, tipo_desvio)     
                self.rota_desvio = self.bfs(self.get_posicao(), destino)
                self.desviando = True
                movimento = self.desviar() # executa o primeiro movimento do desvio
        else:
            # Executa rota de desvio
            movimento = self.desviar()

        return movimento


    def calcula_posicao_obstaculo(self, movimento):
        posicao_obstaculo = self.simulacao_movimento(self.linha, self.coluna, movimento)
        return posicao_obstaculo


    def calcula_tipo_desvio(self, movimento):
        """Calcula se o obstáculo está no início, meio ou final de uma linha/coluna"""
        posicao_obstaculo = self.calcula_posicao_obstaculo(movimento)
        
        coluna_obstaculo = posicao_obstaculo[1]
        obstaculo_esta_no_limite_horizontal = coluna_obstaculo in {0, len(self.modelo_interno[0]) - 1}

        if movimento in ["baixo", "cima"] and obstaculo_esta_no_limite_horizontal:
            return "inicio"
        elif movimento in {"esquerda", "direita"} and obstaculo_esta_no_limite_horizontal:
            return "fim"
        elif movimento in {"esquerda", "direita"} and not obstaculo_esta_no_limite_horizontal:
            return "meio"


    def calcula_destino(self, linha, coluna, movimento, tipo_desvio):
        """Retorna qual posição final de uma rota de desvio"""
        destino = []

        if tipo_desvio == "inicio":
            if self.ultima_movimentacao_executada == "direita":
                direcao = "esquerda"
            else:
                direcao = "direita"

            destino = self.simulacao_movimento(linha, coluna, movimento)
            destino = self.simulacao_movimento(destino[0], destino[1], direcao)
            self.ultima_movimentacao_executada = direcao

        elif tipo_desvio == "meio":
            destino = self.simulacao_movimento(linha, coluna, movimento)
            destino = self.simulacao_movimento(destino[0], destino[1], movimento)

            if self.modelo_interno[destino[0]][destino[1]] == OBSTACULO: 
                destino = self.calcula_destino(destino[0], destino[1], movimento, tipo_desvio)

        elif tipo_desvio == "fim":
            destino = self.simulacao_movimento(linha, coluna, movimento)
            destino = self.simulacao_movimento(destino[0], destino[1], self.direcao)

            if self.ultima_movimentacao_executada == "direita":
                self.ultima_movimentacao_executada = "esquerda"
            else:
                self.ultima_movimentacao_executada = "direita"                                   
        
        return destino

    def simulacao_movimento(self, linha, coluna, movimento):
        movimentos = {
            "cima": (linha - 1, coluna),
            "baixo": (linha + 1, coluna),
            "esquerda": (linha, coluna - 1),
            "direita": (linha, coluna + 1)
        }

        return movimentos[movimento]

    def checar_colisao_obstaculos(self, movimento):
        """Simula o movimento a ser executado e verifica se haveria colisão com um obstáculo"""
        proxima_posicao = self.simulacao_movimento(self.linha, self.coluna, movimento)
        valor_celula = self.modelo_interno[proxima_posicao[0]][proxima_posicao[1]]

        if valor_celula == OBSTACULO:
            return True
        else:
            return False

    def desviar(self):
        """Retorna qual a próxima movimentação a ser feita para executar a rota de desvio"""
        destino = self.rota_desvio[0]

        proximo_movimento = ""
        if destino == cima(*self.get_posicao()):
            proximo_movimento = "cima"
        elif destino == baixo(*self.get_posicao()):
            proximo_movimento = "baixo"
        elif destino == esquerda(*self.get_posicao()):
            proximo_movimento = "esquerda"
        elif destino == direita(*self.get_posicao()):
            proximo_movimento = "direita"
        
        self.rota_desvio = self.rota_desvio[1:]

        return proximo_movimento

    def bfs(self, origem, destino):
        caminho = algoritmo_bfs(origem, destino, self.modelo_interno)
        return caminho

    def zigue_zague(self):
        nova_direcao, proximo_movimento = zigue_zague(self.get_posicao(),
                                        self.ultima_movimentacao_executada,
                                        self.direcao, self.modelo_interno)
        self.direcao = nova_direcao
        return proximo_movimento
        
    def mover(self, acao):
        if self.bateria <= 0:
            return
        
        if acao == "direita":
            self.coluna += 1

        elif acao == "esquerda": 
            self.coluna -= 1

        elif acao == "cima": 
            self.linha -= 1

        elif acao == "baixo": 
            self.linha += 1

        if not self.desviando:
            self.ultima_movimentacao_executada = acao
        self.bateria -= 1
        return self.get_posicao()

    def limpar(self, estado_do_piso):
        if self.bateria > 5:
            if estado_do_piso == PISO_SUJO:
                self.bateria -= 5
                self.contadores[self.linha][self.coluna] += 1
                self.limpezas_efetuadas += 1
                return True

        return False
        


    def recarregar(self):
        if self.posicao_carregador == self.get_posicao():
            self.bateria = self.capacidade_bateria
            return True
        return False


    def calcular_possiveis_hotspots(self):
        limpezas_celulas = {(lin, col): 0 for lin in range(10) for col in range(10)}

        for lin, linha in enumerate(self.contadores):
            for col, cont_limpeza in enumerate(linha):
                limpezas_celulas[(lin, col)] = cont_limpeza
    

        celulas_ordenadas = []
        
        for coord in sorted(limpezas_celulas, key=limpezas_celulas.get, reverse=True):
            celulas_ordenadas.append((coord, limpezas_celulas[coord]))
        
        maior_limpeza = celulas_ordenadas[0][1]
        hotspots = list(filter(lambda x: x[1] >= (maior_limpeza - 2) and x[1]!=0, celulas_ordenadas))
        hotspots = list(zip(*hotspots))
        return list(hotspots[0])


    def calcular_rota_limpeza(self):
        inicio = self.posicao_carregador
        caminho = [inicio]

        for hotspot in self.possiveis_hotspots:
            caminho.extend(self.bfs(inicio, hotspot))
            inicio = hotspot

        caminho.extend(self.bfs(inicio, self.posicao_carregador))
        return caminho


    def get_posicao(self):
        return (self.linha, self.coluna)


    def set_posicao(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna


    def get_bateria(self):
        return self.bateria


    def adiciona_posicao_carregador(self, linha, coluna):
        self.posicao_carregador = (linha, coluna)


    def gerar_status(self, coordenadas_percepcao):
        """Cria representação da posição do agente, modelo interno do ambiente e os contadores"""
        representacao_modelo_interno = self.gerar_representacao_agente(coordenadas_percepcao)
        representacao_contadores = self.gerar_representacao_contadores()
        return concatenar_representacoes(representacao_modelo_interno, representacao_contadores)


    def gerar_representacao_agente(self, coordenadas_percepcao):
        representacao = gerar_cabecalho_matriz("Modelo Interno do Agente", len(self.modelo_interno[0]))

        for l, linha in enumerate(self.modelo_interno):
            representacao += f"{l}|"
            for c in range(len(linha)):
                valor_celula = self.modelo_interno[l][c]
                representacao_celula = colorir_celula(l, c, valor_celula,
                                                      self.get_posicao(), self.posicao_carregador,
                                                      self.possiveis_hotspots, coordenadas_percepcao)
                representacao += representacao_celula
            representacao += "|\n"
        
        return representacao


    def gerar_representacao_contadores(self):
        representacao = gerar_cabecalho_matriz("Contadores", len(self.contadores[0]))

        for l, linha in enumerate(self.contadores):
            representacao += f"{l}|"
            for celula in linha:
                representacao += f"{celula:^3}"
            representacao += "|\n"
        
        return representacao
