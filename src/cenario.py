import numpy as np

from exibir_estado import imprime_estado_simulacao

class Sala:
    vazio = 0
    obstaculo = 1
    sujeira = 2
    direcao_do_aspirador = "direita"

    def __init__(self, tamanho_sala, lista_obstaculos, hot_spots_sujeira, aspirador, posicao_aspirador, posicao_base_recarregamento):
        self.piso = np.zeros(list(tamanho_sala), int)
        self.posicao_agente = list(posicao_aspirador)
        self.posicao_base_carregamento = list(posicao_base_recarregamento)
        self.aspirador = aspirador
        self.lista_obstaculos = lista_obstaculos
        self.hot_spots_sujeira = hot_spots_sujeira
        imprime_estado_simulacao(
            self.piso, self.aspirador.piso, self.posicao_agente,
            self.posicao_base_carregamento, self.hot_spots_sujeira,
            self.lista_obstaculos
        )
    def recuperar_estado_piso(self, coordenada):
        """Mostra o que em uma célula da sala em uma determinada posição"""
        x = coordenada[0]
        y = coordenada[1]
        return self.piso[x][y]

    def adiciona_sujeira(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]
        # n = np.random.random_integers(0, 100)

        # if coordenada in self.hot_spots_sujeira:
        #     if n <= 30:
        #         self.piso[x][y] = 2
        # else:
        #     if n <= 5:
        #         self.piso[x][y] = 2

        self.piso[x][y] = 2

    def remove_sujeira(self, coordenada):
        x = coordenada[0]
        y = coordenada[1]
        self.piso[x][y] = 0

    def percept(self, agent_position):
        """Mostra para o agente o estado do piso na posição dele"""
        return self.recuperar_estado_piso(agent_position)

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
            print('Agent Position: ', self.posicao_agente)
            print(f'Bateria do Agente: {self.aspirador.bateria}')
            imprime_estado_simulacao(
                self.piso, self.aspirador.piso, self.posicao_agente,
                self.posicao_base_carregamento, self.hot_spots_sujeira,
                self.lista_obstaculos
            )

    def execute_action(self, agent, action):
        '''Changes the state of the environment based on what the agent does.'''
        if action == "walk":
            self.posicao_agente, self.direcao_do_aspirador = list(agent.update_position(self.direcao_do_aspirador))

        elif action == "clean":
            estado_do_piso = self.recuperar_estado_piso(agent.location)
            if estado_do_piso == self.sujeira:
                self.remove_sujeira(agent.location)
                agent.clean(estado_do_piso)
            
