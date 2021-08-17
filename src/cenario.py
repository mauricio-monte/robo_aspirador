import numpy as np
import time

from exibir_estado import imprime_estado_simulacao

class Sala:
    vazio = 0
    obstaculo = 1
    sujeira = 2
    direcao_do_aspirador = "direita"
    probabilidade_de_sujeira = 1
    probabilidade_de_sujeira_hot_spot = 10

    def __init__(self, tamanho_sala, lista_obstaculos, hot_spots_sujeira, aspirador, posicao_aspirador, posicao_base_recarregamento):
        self.piso = np.zeros(list(tamanho_sala), int)
        self.posicao_agente = list(posicao_aspirador)
        self.posicao_base_carregamento = list(posicao_base_recarregamento)
        self.aspirador = aspirador
        self.lista_obstaculos = lista_obstaculos
        self.adiciona_obstaculos()
        self.hot_spots_sujeira = hot_spots_sujeira
        imprime_estado_simulacao(
            self.piso, self.aspirador.piso, self.posicao_agente,
            self.posicao_base_carregamento, self.hot_spots_sujeira,
            self.lista_obstaculos
        )
        
    def recuperar_estado_piso(self, coordenada):
        """Mostra o que tem uma célula da sala em uma determinada posição"""
        y = coordenada[0]
        x = coordenada[1]
        if(x>=0 and y>=0):
            if(len(self.piso) > y and len(self.piso[0]) > x):
                return self.piso[x][y]
        return -1

    def suja_tudo(self):
        for i in range(0, len(self.piso)):
            for j in range(0, len(self.piso[0])):
                numero_aleatorio = np.random.random_integers(100)
                if([i, j] in self.hot_spots_sujeira):
                    if(numero_aleatorio <=self.probabilidade_de_sujeira_hot_spot):
                        self.adiciona_sujeira([i,j])
                else:
                     if(numero_aleatorio <= self.probabilidade_de_sujeira):
                        self.adiciona_sujeira([i,j])
                # if probabilidade_de_sujeira <= numero_aleatorio 
                #     adiciona_sujeira([])

    def adiciona_sujeira(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]
        self.piso[x][y] = 2

    def adiciona_obstaculos(self):
        for coordenada in self.lista_obstaculos:
            x = coordenada[0]
            y = coordenada[1]
            self.piso[x][y] = 1

    def get_agent_position(self):
        print(f'Agent Position: (x={self.posicao_agente[1]}, y={self.posicao_agente[0]})')

    def remove_sujeira(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]
        self.piso[x][y] = 0

    def percept(self, agent_position):
        """Mostra para o agente o estado do piso na posição dele"""
        y = agent_position[0]
        x = agent_position[1]

        atual = self.recuperar_estado_piso([y,x])
        cima = self.recuperar_estado_piso([y - 1,x])
        direita = self.recuperar_estado_piso([y,x + 1])
        baixo = self.recuperar_estado_piso([y + 1,x])
        esquerda =self.recuperar_estado_piso([y,x - 1])
        
        return [atual, cima, direita, baixo, esquerda]

    def step(self):
        acao_agente = self.aspirador.program(self.percept(self.posicao_agente))
        print(acao_agente)
        self.execute_action(self.aspirador, acao_agente)

    def run(self, steps=50):  # chama step N vezes para simular o agente e o seu ambiente
        for step in range(steps):
            if self.aspirador.bateria<=0:
                return
            print('\nxxxxxxxxxxxxxxxxxxxx Step ', step+1, ' xxxxxxxxxxxxxxxxxxxx')
            self.step()
            self.get_agent_position()
            print(f'Bateria do Agente: {self.aspirador.bateria}')
            self.suja_tudo()
            imprime_estado_simulacao(
                self.piso, self.aspirador.piso, self.posicao_agente,
                self.posicao_base_carregamento, self.hot_spots_sujeira,
                self.lista_obstaculos
            )
            time.sleep(1)

    def execute_action(self, agent, action):
        '''Changes the state of the environment based on what the agent does.'''
        if action == "walk":
            self.posicao_agente, self.direcao_do_aspirador = list(agent.update_position(self.direcao_do_aspirador))

        elif action == "clean":
            estado_do_piso = self.recuperar_estado_piso(agent.location)
            if estado_do_piso == self.sujeira:
                self.remove_sujeira(agent.location)
                agent.clean(estado_do_piso)
            
