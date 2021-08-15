from aspirador import Aspirador
from cenario import Sala

tamanho_sala = (10, 10)
bateria = 100
array_teste = []

aspirador = Aspirador(bateria, tamanho_sala)

sala = Sala(tamanho_sala, [], [], aspirador, (0,0), (5,5))

sala.adiciona_sujeira((0,1))
sala.adiciona_sujeira((5,5))
sala.adiciona_sujeira((0,9))
sala.adiciona_sujeira((2,5))

sala.remove_sujeira((5,5))


sala.run(20)
