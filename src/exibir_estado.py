import numpy as np
from cores import Cores

NAO_EXPLORADO = 5

def imprime_estado_simulacao(estado_sala, modelo_ambiente, posicao_aspirador, posicao_carregador, hotspots, obstaculos):
        titulos_matrizes = "              Sala                  Sala, dentro do aspirador                Contadores"
        representacao = ""
        for n_linha in range(len(estado_sala)):
            representacao += "|"
            for n_coluna in range(len(estado_sala[0])):
                valor_celula = estado_sala[n_linha][n_coluna]
                cor = ""

                if [n_linha, n_coluna] == posicao_aspirador:
                    cor = Cores.bgBlue
                elif [n_linha, n_coluna] == posicao_carregador:
                    cor = Cores.bgGreen
                elif [n_linha, n_coluna] in hotspots:
                    cor = Cores.fgRed
                elif [n_linha, n_coluna] in obstaculos:
                    cor = Cores.bgBrightRed
                else:
                    cor = Cores.fgWhite
                representacao += cor + " " + str(valor_celula) + " " + Cores.reset  
            representacao += "|  "

            representacao += "|"
            for n_coluna in range(len(modelo_ambiente[0])):
                valor_celula = modelo_ambiente[n_linha][n_coluna]
                cor = ""

                if [n_linha, n_coluna] == posicao_aspirador:
                    cor = Cores.bgBlue
                elif [n_linha, n_coluna] == posicao_carregador:
                    cor = Cores.bgGreen
                elif [n_linha, n_coluna] in hotspots:
                    cor = Cores.fgRed
                elif [n_linha, n_coluna] in obstaculos:
                    cor = Cores.bgBrightRed
                else:
                    if valor_celula == NAO_EXPLORADO:
                        cor = Cores.fgWhite
                    else:
                        cor = Cores.fgBrightWhite

                representacao += cor + " " + str(valor_celula) + " " + Cores.reset  
            representacao += "|  \n"

        print(titulos_matrizes)
        print(representacao)
