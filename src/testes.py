from aspirador import Aspirador
from cenario import Sala


def teste_professor():
    # Código de teste
    ######################
    #criar aspirador com 100% de energia
    M=10
    N=10
    meu_aspirador = Aspirador(100, M,N)

    #cria o ambiente contendo o meu aspirador
    ambiente  = Sala((M,N), [(5,5),(5,4),(5,3)],[(2,2),(3,3)], meu_aspirador, (0,0), (0,0))

    #sumila 100 passos do ambiente
    ambiente.run(100)


def teste_nosso():
    tamanho_sala = (10, 10)
    bateria = 10000
    array_de_obstaculos =[[1, 9]] # [[0, 1], [3, 0]]
    hot_spots_sujeira = [[0, 2], [3, 3]]

    aspirador = Aspirador(bateria, tamanho_sala)

    # Perguntar para o professor sobre as coordenadas usadas para inicializar o ambiente: as tuplas são do formato é (x, y) ou (linha, coluna)?
    sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0, 0), (4, 5))

    sala.run(400)
