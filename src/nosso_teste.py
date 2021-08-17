from aspirador import Aspirador
from cenario import Sala

tamanho_sala = (5, 5)
bateria = 100
array_teste = []
hot_spots_sujeira = [[0,2], [3,3]]

aspirador = Aspirador(bateria, tamanho_sala)

sala = Sala(tamanho_sala, [], hot_spots_sujeira, aspirador, (0,0), (4,4))

sala.run(100)
