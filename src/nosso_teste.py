from aspirador import Aspirador
from cenario import Sala

tamanho_sala = (10, 10)
bateria = 100
array_de_obstaculos = [[0,1], [3,0]]
hot_spots_sujeira = [[0,2], [3,3]]

aspirador = Aspirador(bateria, tamanho_sala)

# Perguntar para o professor sobre as coordenadas usadas para inicializar o ambiente: as tuplas são do formato é (x, y) ou (linha, coluna)?
sala = Sala(tamanho_sala, array_de_obstaculos, hot_spots_sujeira, aspirador, (0,0), (4,5))

sala.run(20)
