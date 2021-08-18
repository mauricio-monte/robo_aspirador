from aspirador import Aspirador
from cenario import Sala

tamanho_sala = (4, 5)
bateria = 100
array_de_obstaculos = [[0,1], [3,0]]
# PERGUNTAR A MAURICIO SE É COORDENADAS (0,2) OU SE É LINHA 0 COLUNA 2
hot_spots_sujeira = [[0,2], [3,3]]

aspirador = Aspirador(bateria, tamanho_sala)

sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0,0), (4,4))

sala.run(10)
