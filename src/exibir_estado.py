import numpy as np
from cores import Cores


def imprime_estado_simulacao(estado_sala, modelo_ambiente, contadores,
                             posicao_aspirador, posicao_carregador, hotspots,
                             obstaculos, percepcao_aspirador, previsao_hotspots=[]):
        titulos_matrizes = "              Sala                  Sala, dentro do aspirador                Contadores"
        representacao = ""
        # Linha da matriz da sala
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
                elif [n_linha, n_coluna] in coordenadas_percepcao(*posicao_aspirador):
                    cor = Cores.fgYellow

                representacao += cor + " " + str(valor_celula) + " " + Cores.reset  
            representacao += "|              "
            
            # Linha da representação da sala criada pelo aspirador
            representacao += "|"
            for n_coluna in range(len(modelo_ambiente[0])):
                valor_celula = modelo_ambiente[n_linha][n_coluna]
                cor = ""

                if [n_linha, n_coluna] == posicao_aspirador:
                    cor = Cores.bgBlue
                elif [n_linha, n_coluna] == posicao_carregador:
                    cor = Cores.bgGreen
                elif [n_linha, n_coluna] in previsao_hotspots:
                    cor = Cores.fgRed
                elif [n_linha, n_coluna] in obstaculos:
                    cor = Cores.bgBrightRed
                elif [n_linha, n_coluna] in coordenadas_percepcao(*posicao_aspirador):
                    cor = Cores.fgYellow

                representacao += cor + " " + str(valor_celula) + " " + Cores.reset  
            representacao += "|              "

            # Linha da matriz de contadores
            representacao += "|"
            for n_coluna in range(len(contadores[0])):
                valor_celula = contadores[n_linha][n_coluna]

                representacao += " " + str(valor_celula) + " "
            representacao += "|  \n"

        print(titulos_matrizes)
        print(representacao)

def coordenadas_percepcao(linha, coluna):
    return [[linha - 1, coluna], [linha, coluna + 1], [linha + 1, coluna], [linha, coluna - 1]]
