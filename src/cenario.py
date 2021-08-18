import numpy as np
import time

from exibir_estado import imprime_estado_simulacao

class Sala:
    vazio = 0
    obstaculo = 1
    sujeira = 2
    direcao_do_aspirador = "direita"
    probabilidade_de_sujeira = 1
    probabilidade_de_sujeira_hot_spot = 10

    def __init__(self, tamanho_sala, lista_obstaculos, hot_spots_sujeira,
                 aspirador, posicao_aspirador, posicao_base_recarregamento):
        linhas = tamanho_sala[0]
        colunas = tamanho_sala[1]
        self.piso = np.zeros([linhas, colunas], int)
        self.posicao_agente = list(posicao_aspirador)
        self.posicao_base_carregamento = list(posicao_base_recarregamento)
        self.aspirador = aspirador
        self.lista_obstaculos = lista_obstaculos
        self.hot_spots_sujeira = hot_spots_sujeira
        self.adiciona_obstaculos()

        
    def recuperar_estado_piso(self, linha, coluna):
        """Mostra o que tem uma célula da sala em uma determinada posição"""       
        if(coluna>=0 and linha>=0):
            if(len(self.piso) > linha and len(self.piso[0]) > coluna):
                return self.piso[linha][coluna]
        return -1

    def suja_tudo(self):
        for i in range(0, len(self.piso)):
            for j in range(0, len(self.piso[0])):
                numero_aleatorio = np.random.random_integers(100)
                if([i, j] in self.hot_spots_sujeira):
                    if(numero_aleatorio <=self.probabilidade_de_sujeira_hot_spot):
                        self.adiciona_sujeira(i,j)
                else:
                     if(numero_aleatorio <= self.probabilidade_de_sujeira):
                        self.adiciona_sujeira(i,j)
                # if probabilidade_de_sujeira <= numero_aleatorio 
                #     adiciona_sujeira([])

    def adiciona_sujeira(self, linha, coluna):
        self.piso[linha][coluna] = 2

    def adiciona_obstaculos(self):
        for coordenada in self.lista_obstaculos:
            linha = coordenada[0]
            coluna = coordenada[1]
            self.piso[linha][coluna] = 1

    def get_agent_position(self):
        return (f'Agent Position: (x={self.posicao_agente[1]}, y={self.posicao_agente[0]})')

    def remove_sujeira(self, linha, coluna):
        self.piso[linha][coluna] = 0

    def percept(self, agent_position):
        """Mostra para o agente o estado do piso na posição dele"""
        linha = agent_position[0]
        coluna = agent_position[1]
        
        return {
            "atual": self.recuperar_estado_piso(linha, coluna),
            "cima": self.recuperar_estado_piso(linha - 1, coluna),
            "direita": self.recuperar_estado_piso(linha, coluna + 1),
            "baixo": self.recuperar_estado_piso(linha + 1, coluna),
            "esquerda": self.recuperar_estado_piso(linha, coluna - 1)
        }

    def step(self):
        estado_pisos_percepcao = self.percept(self.posicao_agente)
        acao_agente = self.aspirador.program(estado_pisos_percepcao)
        print("Ação agente", acao_agente)
        self.execute_action(self.aspirador, acao_agente)

    def run(self, steps=50):  # chama step N vezes para simular o agente e o seu ambiente
        print('\nxxxxxxxxxxxxxxxxxxxx Estado Inicial xxxxxxxxxxxxxxxxxxxx')
        print(f'Agente:{self.get_agent_position()} Bateria: {self.aspirador.bateria}')
        imprime_estado_simulacao(
                self.piso, self.aspirador.piso, self.posicao_agente,
                self.posicao_base_carregamento, self.hot_spots_sujeira,
                self.lista_obstaculos
            )
        time.sleep(1)
        for step in range(steps):
            if self.aspirador.bateria<=0:
                return
            self.suja_tudo()
            self.step() 

            print(f'Agente:{self.get_agent_position()} Bateria: {self.aspirador.bateria}')
            print('\nxxxxxxxxxxxxxxxxxxxx Step ', step+1, ' xxxxxxxxxxxxxxxxxxxx')
            imprime_estado_simulacao(
                self.piso, self.aspirador.piso, self.posicao_agente,
                self.posicao_base_carregamento, self.hot_spots_sujeira,
                self.lista_obstaculos
            )
            time.sleep(1)

    def execute_action(self, agent, action):
        '''Changes the state of the environment based on what the agent does.'''
        if action == "walk":
            self.posicao_agente, self.direcao_do_aspirador = list(agent.update_position(self.direcao_do_aspirador))

        elif action == "clean":
            linha = agent.location[0]
            coluna = agent.location[1]
            estado_do_piso = self.recuperar_estado_piso(linha, coluna)
            if estado_do_piso == self.sujeira:
                self.remove_sujeira(linha, coluna)
                agent.clean(estado_do_piso)
            
