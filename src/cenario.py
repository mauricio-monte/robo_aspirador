import numpy as np


class Sala
    vazio = 0
    obstáculo = 1
    sujeira = 2
    piso = np.array([M, N], int)
    hot_spots_sujeira = np.array([]), int)  # onde há sujeira
    int
    pos_aspirador(x, y)
    int
    pos_base(x, y)

    def __init__((M, N), lista_obstáculos, hot_spots_sujeira, aspirador, posição_aspirador, posição_base_recarregamento)

    # Escreva seu código aqui levando em conta que:
    # o piso recebe valor vazio em todo lugar e
    # você deve colocar obstáculos nas coordenadas recebidas no 2o parâmetro do construtor
    # a sujeira deve ser atualizada no método step() pois, mesmo quando o agente limpa,
    # a sujeira deverá reaparecer com certa probabilidade

    def step()  # atualiza sujeira, realiza a interação do agente-ambiente
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

        def run(N)  # chama step N vezes para simular o agente e o seu ambiente