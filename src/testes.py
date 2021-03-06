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
    ambiente.run(500)


def teste_nosso():
    M=10
    N=10
    meu_aspirador = Aspirador(100, M, N)
    posicao_aspirador = (0,0)
    posicao_base_carregador = (4,5)
    posicao_obstaculos = [(5,5),(5,4),(5,3), (1,9), (2,0)]
    posicao_hotspots = [(2,2),(3,3), (2,3), (7,7)]
    ambiente  = Sala((M,N), posicao_obstaculos, posicao_hotspots, meu_aspirador, posicao_aspirador, posicao_base_carregador)
    ambiente.run(400)

def teste_obstaculo_inicio_linha_horizontal():
    tamanho_sala = (10, 10)
    bateria = 10000
    array_de_obstaculos = [[1, 9]]
    rota_desvio = [(0,8), (1,8)] # Essa é a rota que se espera que seja retornada pela bfs
    hot_spots_sujeira = [[0, 2], [3, 3]]
    aspirador = Aspirador(bateria, tamanho_sala)

    sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0, 0), (4, 5))

    sala.run(500)

def teste_obstaculo_meio_linha_horizontal():
    tamanho_sala = (10, 10)
    bateria = 100
    array_de_obstaculos = [[0, 5]]
    rota_desvio = [(1, 4), (1, 5), (1, 6), (0, 6)] # Essa é a rota que se espera que seja retornada pela bfs
    hot_spots_sujeira = [[0, 2], [3, 3]]
    aspirador = Aspirador(bateria, tamanho_sala)

    sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0, 0), (4, 5))

    sala.run(500)

def teste_obstaculo_meio2_linha_horizontal():
    tamanho_sala = (10, 10)
    bateria = 10000
    array_de_obstaculos = [[1, 5]]
    rota_desvio = [(1, 4), (1, 5), (1, 6), (0, 6)] # Essa é a rota que se espera que seja retornada pela bfs
    hot_spots_sujeira = [[0, 2], [3, 3]]
    aspirador = Aspirador(bateria, tamanho_sala)

    sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0, 0), (4, 5))

    sala.run(500)

def teste_obstaculo_final_linha_horizontal():
    tamanho_sala = (10, 10)
    bateria = 10000
    array_de_obstaculos = [[0, 9]] 
    rota_desvio = [(1,8), (1,9)] # Essa é a rota que se espera que seja retornada pela bfs
    hot_spots_sujeira = [[0, 2], [3, 3]]
    aspirador = Aspirador(bateria, tamanho_sala)

    sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0, 0), (4, 5))

    sala.run(500)
