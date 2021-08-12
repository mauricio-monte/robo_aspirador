import numpy as np


class Sala:
    vazio = 0
    obstáculo = 1
    sujeira = 2

    def __init__(self, dimensoes_matriz, lista_obstaculos, hot_spots_sujeira, aspirador, posicao_aspirador, posicao_base_recarregamento):
        self.M = dimensoes_matriz[0]
        self.N = dimensoes_matriz[1]
        self.piso = np.array([self.M, self.N], int)
        self.hot_spots_sujeira = np.array(hot_spots_sujeira, int)  # onde há sujeira
        self.pos_aspirador = (posicao_aspirador[0], posicao_aspirador[1])
        self.pos_base = (posicao_base_recarregamento[0], posicao_base_recarregamento[1])

    # Escreva seu código aqui levando em conta que:
    # o piso recebe valor vazio em todo lugar e
    # você deve colocar obstáculos nas coordenadas recebidas no 2o parâmetro do construtor
    # a sujeira deve ser atualizada no método step() pois, mesmo quando o agente limpa,
    # a sujeira deverá reaparecer com certa probabilidade

    def step(self):  # atualiza sujeira, realiza a interação do agente-ambiente
        # Escreva seu código aqui levando em conta o pseudo-código para
        # adicionar sujeira com maior probabilidade em certos locais:

        # atualização da sujeira
        # for i até dim M
        #  for j até dim N
        #      r = rand(0,1)
        #      se (i,j) pertence a hot_spots_sujeira
        #      então
        #            se r < 0.1 então piso(i,j) = sujeira
        #      senão se r < 0.01 então piso(i,j) = sujeira

        # chamar o programa do agente e atualiza suas coordenadas a partir da
        # ação recomendada pelo próprio agente
        # imprimir o estado do ambiente
        # imprimir o estado do Agente aspirador
        pass

    def run(self, N):  # chama step N vezes para simular o agente e o seu ambiente
        pass