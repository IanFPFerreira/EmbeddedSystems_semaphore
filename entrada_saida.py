cruzamento_1 = {
    'Verde_principal': 20,
    'Amarelo_principal': 16,
    'Vermelho_principal': 12,
    'Verde_auxiliar': 1,
    'Amarelo_auxiliar': 26,
    'Vermelho_auxiliar': 21,
    'Pedestre_principal': 7,
    'Pedestre_auxiliar': 8,
    'Passagem_1': 14,
    'Passagem_2': 15,
    'Velocidade_1_A': 18,
    'Velocidade_1_B': 23,
    'Velocidade_2_A': 24,
    'Velocidade_2_B': 25 
    }

cruzamento_2 = {
    'Verde_principal': 2,
    'Amarelo_principal': 3,
    'Vermelho_principal': 11,
    'Verde_auxiliar': 0,
    'Amarelo_auxiliar': 5,
    'Vermelho_auxiliar': 6,
    'Pedestre_principal': 9,
    'Pedestre_auxiliar': 10,
    'Passagem_1': 4,
    'Passagem_2': 17,
    'Velocidade_1_A': 27,
    'Velocidade_1_B': 22,
    'Velocidade_2_A': 13,
    'Velocidade_2_B': 19 
    }

botao_pedestre_principal, botao_pedestre_auxiliar = False, False
sensor_passagem, verifica_passagem = False, False
sensor_parada, verifica_parada = False, False
sensor_velocidade, verifica_velocidade = False, False
tempo_inicial, tempo_final = 0.0, 0.0
tempo_semaforo = 0
