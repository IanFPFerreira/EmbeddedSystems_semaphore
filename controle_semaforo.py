from datetime import datetime

from comportamento_semaforo import *
from entrada_saida import *


dict_rotinas = {'principal_verde': [principal_verde, 40], 
                'auxiliar_verde': [auxiliar_verde, 20],
                'todos_vermelho': [todos_vermelho, 2],
                'principal_amarelo': [principal_amarelo, 3]}


def verifica_entradas_saidas(semaforo, cruzamento, tempo_sleep=0.5):
    global botao_pedestre_principal, botao_pedestre_auxiliar
    global sensor_passagem, verifica_passagem
    global sensor_parada, verifica_parada
    global tempo_semaforo

    tempo_semaforo = 0
    while tempo_semaforo < dict_rotinas[semaforo][1]:
        dict_rotinas[semaforo][0](cruzamento)
        sleep(tempo_sleep)
        tempo_semaforo += 1
        if semaforo == 'principal_verde':
            print(tempo_semaforo, botao_pedestre_principal, verifica_passagem)
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and botao_pedestre_principal:
                break
            if tempo_semaforo >= dict_rotinas[semaforo][1]/2 and sensor_passagem:
                break
            if tempo_semaforo <= dict_rotinas[semaforo][1]/2 and verifica_passagem:
                verifica_passagem = False
                print('Multado')
        elif semaforo == 'auxiliar_verde':
            print(tempo_semaforo, botao_pedestre_auxiliar, verifica_parada)
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
                print('Multado')
        elif semaforo == 'principal_amarelo':
            if verifica_passagem:
                verifica_passagem = False
                print('Multado')

        
def rotina_semaforo(cruzamento):
    global botao_pedestre_principal, botao_pedestre_auxiliar
    global sensor_passagem, verifica_passagem
    global sensor_parada, verifica_parada

    while True:
        # todos_vermelho(cruzamento)
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('todos_vermelho', cruzamento)
        
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('principal_verde', cruzamento)
        sensor_passagem, verifica_passagem = False, False
        botao_pedestre_principal = False

        # principal_amarelo(cruzamento)
        verifica_passagem = False
        verifica_entradas_saidas('principal_amarelo', cruzamento, 1)        

        # todos_vermelho(cruzamento)
        sensor_passagem, verifica_passagem = False, False
        verifica_entradas_saidas('todos_vermelho', cruzamento)

        sensor_parada, verifica_parada = False, False
        verifica_entradas_saidas('auxiliar_verde', cruzamento)
        sensor_parada, verifica_parada = False, False        
        botao_pedestre_auxiliar = False

        auxiliar_amarelo(cruzamento)


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
    print(f"Sensor Inicial: {channel} ____ Ativado: {tempo_inicial}")


def sensor_parada_semaforo_principal(channel):
    global sensor_parada, verifica_parada, sensor_velocidade, tempo_inicial, tempo_final
    if not sensor_velocidade:
        sensor_velocidade = False
        if GPIO.input(channel):
            sensor_parada = True
        if not GPIO.input(channel):
            verifica_parada = True
        print(f"Sensor: {channel}")
    else:
        sensor_velocidade = False
        h, m, s = datetime.now().strftime('%H:%M:%S.%f').split(':')
        tempo_final = int(h) * 3600 + int(m) * 60 + float(s)
        tempo_total = tempo_final - tempo_inicial
        print(f"Sensor Final: {channel}  ____ Ativado: {tempo_final}")
        print(f"Tempo Total: {tempo_total}")
        print(f"Velocidade: {(1 / tempo_total) * 3.6}")	
