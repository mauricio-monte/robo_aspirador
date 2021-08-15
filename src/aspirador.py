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
        if estado_piso == PISO_SUJO:
            return 'clean'
        return 'walk'

    def update_position(self):
        y = self.location[0]
        x = self.location[1]
        direcao = "direita"
        
        if direcao == "direita":
            if y < len(self.piso[0]) - 1:
                self.location[1] += 1
            else:
                direcao = "baixo"

        elif direcao == "esquerda": 
            if  x == 0:
                self.location[1] -= 1
            else:
                direcao = "cima"

        elif direcao == "cima": 
            if y == 0:
                self.location[0] -= 1
            else:
                direcao = "direita"

        elif direcao == "baixo": 
            if y < len(self.piso) - 1:
                self.location[0] += 1
            else:
                direcao = "esquerda"

        self.bateria -= 1
        return self.location

    def clean(self, estado_do_piso):
        if estado_do_piso == PISO_SUJO:
            self.bateria -= 5
            return True
        return False

    def get_bateria(self):
        return self.bateria

    # realizar busca heurística usando a avaliação heurística, o modelo do ambiente e a percepção corrente.
    # considerar que ele deve retornar à base quando a bateria estiver crítica

    def print_status():  # imprime posição do agente, o seu modelo interno do ambiente, nível da bateria
        pass
