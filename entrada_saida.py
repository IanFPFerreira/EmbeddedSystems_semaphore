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
    'Verde_principal': 0,
    'Amarelo_principal': 5,
    'Vermelho_principal': 6,
    'Verde_auxiliar': 2,
    'Amarelo_auxiliar': 3,
    'Vermelho_auxiliar': 11,
    'Pedestre_principal': 9,
    'Pedestre_auxiliar': 10,
    'Passagem_1': 4,
    'Passagem_2': 17,
    'Velocidade_1_A': 27,
    'Velocidade_1_B': 22,
    'Velocidade_2_A': 19,
    'Velocidade_2_B': 13 
}

infos_servidor_central = {
    'Cruzamento': 0,
    'Avanco_sinal_vermelho' : 0,
    'Acima_velocidade_limite' : 0,
    'Media_velocidade' : [0],
    'Numero_veiculos' : 0,
    'Temporizador' : 0,
}


botao_pedestre_principal, botao_pedestre_auxiliar = False, False
sensor_passagem, verifica_passagem = False, False
sensor_parada, verifica_parada = False, False
sensor_velocidade, verifica_velocidade = False, False
tempo_inicial, tempo_final = 0.0, 0.0
tempo_semaforo = 0
modo_noturno_ativo, modo_emergencia_ativo = False, False
