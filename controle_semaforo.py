from datetime import datetime

from comportamento_semaforo import *
from entrada_saida import *


dict_rotinas = {
    'principal_verde': [principal_verde, 40], 
    'auxiliar_verde': [auxiliar_verde, 20],
    'todos_vermelho': [todos_vermelho, 2],
    'principal_amarelo': [principal_amarelo, 6],
    'auxiliar_amarelo': [auxiliar_amarelo, 6]
}


def verifica_entradas_saidas(semaforo, cruzamento, tempo_sleep=0.5):
    global botao_pedestre_principal, botao_pedestre_auxiliar
    global sensor_passagem, verifica_passagem
    global sensor_parada, verifica_parada
    global tempo_semaforo
    global infos_servidor_central
    global modo_noturno_ativo, modo_emergencia_ativo

    tempo_semaforo = 0
    while tempo_semaforo < dict_rotinas[semaforo][1]:

        if modo_noturno_ativo:
            rotina_modo_noturno(cruzamento)
        if modo_emergencia_ativo:
            rotina_modo_emergencia(cruzamento)

        dict_rotinas[semaforo][0](cruzamento)
        sleep(tempo_sleep)
        tempo_semaforo += 1
        if semaforo == 'principal_verde':
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and botao_pedestre_principal:
                break
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and sensor_passagem:
                break
            if tempo_semaforo <= dict_rotinas[semaforo][1]/2 and verifica_passagem:
                verifica_passagem = False
                infos_servidor_central['Avanco_sinal_vermelho'] += 1
                print('Multado')
        elif semaforo == 'auxiliar_verde':
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and botao_pedestre_auxiliar:
                break
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and sensor_parada:
                break
            if tempo_semaforo <= dict_rotinas[semaforo][1]/2 and verifica_parada:
                verifica_parada = False
                print('Multado')
        elif semaforo == 'todos_vermelho':
            if verifica_parada or verifica_passagem:
                verifica_parada, verifica_passagem = False, False
                infos_servidor_central['Avanco_sinal_vermelho'] += 1
                print('Multado')
        elif semaforo == 'principal_amarelo':
            if verifica_passagem:
                verifica_passagem = False
                infos_servidor_central['Avanco_sinal_vermelho'] += 1
                print('Multado')
        elif semaforo == 'auxiliar_amarelo':
            if verifica_parada:
                verifica_parada = False
                infos_servidor_central['Avanco_sinal_vermelho'] += 1
                print('Multado')

        
def rotina_semaforo(cruzamento):
    global botao_pedestre_principal, botao_pedestre_auxiliar
    global sensor_passagem, verifica_passagem
    global sensor_parada, verifica_parada

    while True:
        print('Todos vermelhos')
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('todos_vermelho', cruzamento)
        
        print('Principal verde')
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('principal_verde', cruzamento)
        sensor_passagem, verifica_passagem = False, False
        botao_pedestre_principal = False

        print('Principal amarelo')
        verifica_passagem = False
        verifica_entradas_saidas('principal_amarelo', cruzamento)        

        print('Todos vermelhos')
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('todos_vermelho', cruzamento)

        print('Auxiliar verde')
        sensor_parada, verifica_parada = False, False
        verifica_entradas_saidas('auxiliar_verde', cruzamento)
        sensor_parada, verifica_parada = False, False        
        botao_pedestre_auxiliar = False

        print('Auxiliar amarelo')
        verifica_parada = False
        verifica_entradas_saidas('auxiliar_amarelo', cruzamento)
        verifica_parada = False 


def rotina_modo_noturno(cruzamento):
    global modo_noturno_ativo
    print('Modo noturno ativado')
    while True:
        if not modo_noturno_ativo:
            rotina_semaforo(cruzamento)
        if modo_emergencia_ativo:
            rotina_modo_emergencia(cruzamento)
        modo_noturno(cruzamento)


def rotina_modo_emergencia(cruzamento):
    global botao_pedestre_principal, botao_pedestre_auxiliar
    global sensor_passagem, verifica_passagem
    global sensor_parada, verifica_parada
    global modo_emergencia_ativo

    sensor_passagem, verifica_passagem = False, False
    print('Modo emergencia ativado')
    while True:
        if not modo_emergencia_ativo:
            rotina_semaforo(cruzamento)
        if modo_noturno_ativo:
            rotina_modo_noturno(cruzamento)
        principal_verde(cruzamento)
        if verifica_passagem:
            sensor_passagem, verifica_passagem = False, False
            infos_servidor_central['Avanco_sinal_vermelho'] += 1
            print('Multado')


def verifica_modo_servidor(modo):
    global modo_noturno_ativo, modo_emergencia_ativo
    if modo == '1' or modo == '3':
        modo_emergencia_ativo = True
    elif modo == '2' or modo == '4':
        modo_emergencia_ativo = False
    elif modo == '5':
        modo_noturno_ativo = True
    elif modo == '6':
        modo_noturno_ativo = False


def botao_pedestre_semaforo_principal(channel):
    global botao_pedestre_principal
    botao_pedestre_principal = True
    print(f"Botao: {channel}")


def botao_pedestre_semaforo_auxiliar(channel):
    global botao_pedestre_auxiliar
    botao_pedestre_auxiliar = True
    print(f"Botao: {channel}")


def sensor_passagem_semaforo_auxiliar(channel):
    global sensor_passagem, verifica_passagem
    if GPIO.input(channel):
        sensor_passagem = True
    if not GPIO.input(channel):
        verifica_passagem = True
    print(f"Sensor: {channel}")


def sensor_velocidade_semaforo_principal(channel):
    global sensor_velocidade, verifica_velocidade, tempo_inicial
    sensor_velocidade = True
    h, m, s = datetime.now().strftime('%H:%M:%S.%f').split(':')
    tempo_inicial = int(h) * 3600 + int(m) * 60 + float(s)
    print(f"Sensor: {channel}")


def sensor_parada_semaforo_principal(channel):
    global sensor_parada, verifica_parada, sensor_velocidade, tempo_inicial, tempo_final
    if not sensor_velocidade:
        sensor_velocidade = False
        if GPIO.input(channel):
            infos_servidor_central['Numero_veiculos'] += 1
            sensor_parada = True
        if not GPIO.input(channel):
            verifica_parada = True
        print(f"Sensor: {channel}")
    else:
        sensor_velocidade = False
        verifica_parada = True
        h, m, s = datetime.now().strftime('%H:%M:%S.%f').split(':')
        tempo_final = int(h) * 3600 + int(m) * 60 + float(s)
        tempo_total = tempo_final - tempo_inicial
        velocidade_total = (1 / tempo_total) * 3.6

        infos_servidor_central['Numero_veiculos'] += 1
        if infos_servidor_central['Media_velocidade'][0] == 0:
            infos_servidor_central['Media_velocidade'][0] = velocidade_total
        else:
            infos_servidor_central['Media_velocidade'].append(velocidade_total)
        if velocidade_total > 60:
            infos_servidor_central['Acima_velocidade_limite'] += 1
        print(f"Sensor: {channel}")
        print(f"Velocidade: {(1 / tempo_total) * 3.6}")	


def enviando_informacoes(tempo):
    global infos_servidor_central
    infos_servidor_central['Temporizador'] += tempo
    return infos_servidor_central
    