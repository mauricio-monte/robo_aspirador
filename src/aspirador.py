import numpy as np


class Aspirador:
    actions = ["frente", "esq", "dir", "tras", "aspirar", "recarregar"]
    status_percepção = ["sujo", "vazio", "obstáculo"]  # diz respeito à celula imediatamente à frente do agente se obstáculo

    def __init__(self, energia_aspirador, M, N):
        self.energia = energia_aspirador
        # consulta o ambiente para obter as coordenadas
        modelo_ambiente = np.array([M, N], int)  # registra as experiências do robô.
        # no modelo é guardado: contador de sujeira (0...MAX) ou obstáculo (-1)
        
        # definida a partir do contador de sujeira e da posição atual.
        avaliação_heurística = np.array([M, N], int)

    def update_posição(nova_posicao):
        pass

    def action_agent_program(percepcao):
        pass

    # realizar busca heurística usando a avaliação heurística, o modelo do ambiente e a percepção corrente.
    # considerar que ele deve retornar à base quando a bateria estiver crítica

    def print_status():  # imprime posição do agente, o seu modelo interno do ambiente, nível da bateria
        pass