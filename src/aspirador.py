import numpy as np

PISO_LIMPO = 0
OBSTACULO = 1
PISO_SUJO = 2

class Aspirador:
    location = [0, 0]
    
    def __init__(self, bateria, tamanho_sala):
        self.bateria = bateria
        self.piso = np.zeros(list(tamanho_sala), str)
        self.piso.fill("?")
        self.contadores = np.zeros(list(tamanho_sala), int)

    def program(self, estado_piso):
        linha = self.location[0]
        coluna = self.location[1]

        if (estado_piso["cima"] in [0, 1, 2]):
            self.piso[linha - 1][coluna] = estado_piso["cima"]
        if (estado_piso["direita"]  in [0, 1, 2]):
            self.piso[linha][coluna + 1] = estado_piso["direita"]
        if (estado_piso["baixo"]  in [0, 1, 2]):
            self.piso[linha + 1][coluna] = estado_piso["baixo"] 
        if (estado_piso["esquerda"] in [0, 1, 2]):
            self.piso[linha][coluna - 1] = estado_piso["esquerda"]
        if (estado_piso["atual"] in [0, 1, 2]):
            self.piso[linha][coluna] = estado_piso["atual"]

        if estado_piso["atual"] == PISO_SUJO:
            return 'clean'
        return 'walk'

    def update_position(self, direcao="direita"):
        if(self.bateria<=0):
            return
        linha = self.location[0]
        coluna = self.location[1]
        
        if direcao == "direita":
            if coluna < len(self.piso[0]) - 1:
                self.location[1] += 1
            else:
                direcao = "baixo"
                self.update_position("baixo")

        elif direcao == "esquerda": 
            if  coluna > 0:
                self.location[1] -= 1
            else:
                direcao = "cima"
                self.update_position("cima")

        elif direcao == "cima": 
            if linha > 0:
                self.location[0] -= 1
            else:
                direcao = "direita"
                self.update_position("direita")

        elif direcao == "baixo": 
            if linha < len(self.piso) - 1:
                self.location[0] += 1
            else:
                direcao = "esquerda"
                self.update_position("esquerda")

        self.bateria -= 1
        return (self.location, direcao)

    def clean(self, estado_do_piso):
        if self.bateria > 5:
            if estado_do_piso == PISO_SUJO:
                self.bateria -= 5

                linha = self.location[0]
                coluna = self.location[1]

                self.contadores[linha][coluna] += 1
                return True
        return False

    def get_bateria(self):
        return self.bateria

    # realizar busca heurística usando a avaliação heurística, o modelo do ambiente e a percepção corrente.
    # considerar que ele deve retornar à base quando a bateria estiver crítica

    def print_status():  # imprime posição do agente, o seu modelo interno do ambiente, nível da bateria
        pass
