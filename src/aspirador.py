import numpy as np

PISO_LIMPO = 0
OBSTACULO = 1
PISO_SUJO = 2

class Aspirador:
    location = [0, 0]
    
    def __init__(self, bateria, tamanho_sala):
        self.bateria = bateria
        self.piso = np.zeros(list(tamanho_sala), int)
    
    def program(self, estado_piso):

        if estado_piso[0] == PISO_SUJO:
            return 'clean'
        return 'walk'

    def update_position(self, direcao="direita"):
        if(self.bateria<=0):
            return
        y = self.location[0]
        x = self.location[1]
        
        if direcao == "direita":
            if x < len(self.piso[0]) - 1:
                self.location[1] += 1
            else:
                direcao = "baixo"
                self.update_position("baixo")

        elif direcao == "esquerda": 
            if  x > 0:
                self.location[1] -= 1
            else:
                direcao = "cima"
                self.update_position("cima")

        elif direcao == "cima": 
            if y > 0:
                self.location[0] -= 1
            else:
                direcao = "direita"
                self.update_position("direita")

        elif direcao == "baixo": 
            if y < len(self.piso) - 1:
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

                y = self.location[0]
                x = self.location[1]

                self.piso[y][x] += 1
                return True
        return False

    def get_bateria(self):
        return self.bateria

    # realizar busca heurística usando a avaliação heurística, o modelo do ambiente e a percepção corrente.
    # considerar que ele deve retornar à base quando a bateria estiver crítica

    def print_status():  # imprime posição do agente, o seu modelo interno do ambiente, nível da bateria
        pass
