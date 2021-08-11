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