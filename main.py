import RPi.GPIO as GPIO
import sys
from threading import Thread
import socket
import json
import time
import sys

from entrada_saida import cruzamento_1, cruzamento_2
from comportamento_semaforo import lista_cruzamento
from controle_semaforo import *

cruzamento = {}

if sys.argv[1] == 'cruzamento_1' or sys.argv[1] == 'cruzamento_3':
    cruzamento = cruzamento_1.copy()
elif sys.argv[1] == 'cruzamento_2' or sys.argv[1] == 'cruzamento_4':
    cruzamento = cruzamento_2.copy()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(lista_cruzamento(cruzamento), GPIO.OUT)

GPIO.setup(cruzamento['Pedestre_principal'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cruzamento['Pedestre_auxiliar'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(cruzamento['Passagem_1'], GPIO.IN)
GPIO.setup(cruzamento['Passagem_2'], GPIO.IN)

GPIO.setup(cruzamento['Velocidade_1_A'], GPIO.IN)
GPIO.setup(cruzamento['Velocidade_2_A'], GPIO.IN)

GPIO.setup(cruzamento['Velocidade_1_B'], GPIO.IN)
GPIO.setup(cruzamento['Velocidade_2_B'], GPIO.IN)


HOST = '192.168.1.129' 
PORT = 10191

try:
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    def enviar_dados():
        while True:
            tempo_inicial = time.perf_counter()
            sleep(10)
            tempo_final = time.perf_counter()
            infos_servidor_central_enviado = enviando_informacoes(tempo_final - tempo_inicial)
            infos_servidor_central_enviado['Cruzamento'] = int(sys.argv[1][-1])
            infos_servidor_central_enviado = json.dumps(infos_servidor_central_enviado).encode('utf-8')
            client_socket.sendall(infos_servidor_central_enviado)


    def receber_dados():
        while True:
            msg = client_socket.recv(1024)
            msg = msg.decode('utf-8')
            print(msg)
            verifica_modo_servidor(msg)


    GPIO.add_event_detect(cruzamento['Pedestre_principal'], GPIO.RISING, callback=botao_pedestre_semaforo_principal, bouncetime=300)
    GPIO.add_event_detect(cruzamento['Pedestre_auxiliar'], GPIO.RISING, callback=botao_pedestre_semaforo_auxiliar, bouncetime=300)

    GPIO.add_event_detect(cruzamento['Passagem_1'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)
    GPIO.add_event_detect(cruzamento['Passagem_2'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)

    GPIO.add_event_detect(cruzamento['Velocidade_1_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)
    GPIO.add_event_detect(cruzamento['Velocidade_2_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)

    GPIO.add_event_detect(cruzamento['Velocidade_1_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)
    GPIO.add_event_detect(cruzamento['Velocidade_2_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)


    thread_cruzamento = Thread(target=rotina_semaforo, args=(cruzamento,))
    thread_cruzamento.start()

    thread_envia_dados = Thread(target=enviar_dados)
    thread_envia_dados.start()

    thread_recebe_dados = Thread(target=receber_dados)
    thread_recebe_dados.start()


except KeyboardInterrupt:
    print("Saindo...")
    client_socket.close()
    sys.exit()
