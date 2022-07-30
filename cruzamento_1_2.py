import RPi.GPIO as GPIO
import sys
from threading import Thread
# import multiprocessing

from entrada_saida import cruzamento_1, cruzamento_2
from comportamento_semaforo import lista_cruzamento
from controle_semaforo import *


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(lista_cruzamento(cruzamento_1), GPIO.OUT)
GPIO.setup(lista_cruzamento(cruzamento_2), GPIO.OUT)


GPIO.setup(cruzamento_1['Pedestre_principal'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cruzamento_1['Pedestre_auxiliar'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cruzamento_2['Pedestre_principal'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cruzamento_2['Pedestre_auxiliar'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(cruzamento_1['Passagem_1'], GPIO.IN)
GPIO.setup(cruzamento_1['Passagem_2'], GPIO.IN)
GPIO.setup(cruzamento_2['Passagem_1'], GPIO.IN)
GPIO.setup(cruzamento_2['Passagem_2'], GPIO.IN)

GPIO.setup(cruzamento_1['Velocidade_1_A'], GPIO.IN)
GPIO.setup(cruzamento_1['Velocidade_2_A'], GPIO.IN)
GPIO.setup(cruzamento_2['Velocidade_1_A'], GPIO.IN)
GPIO.setup(cruzamento_2['Velocidade_2_A'], GPIO.IN)

GPIO.setup(cruzamento_1['Velocidade_1_B'], GPIO.IN)
GPIO.setup(cruzamento_1['Velocidade_2_B'], GPIO.IN)
GPIO.setup(cruzamento_2['Velocidade_1_B'], GPIO.IN)
GPIO.setup(cruzamento_2['Velocidade_2_B'], GPIO.IN)


try:
    GPIO.add_event_detect(cruzamento_1['Pedestre_principal'], GPIO.RISING, callback=botao_pedestre_semaforo_principal, bouncetime=300)
    GPIO.add_event_detect(cruzamento_1['Pedestre_auxiliar'], GPIO.RISING, callback=botao_pedestre_semaforo_auxiliar, bouncetime=300)
    GPIO.add_event_detect(cruzamento_2['Pedestre_principal'], GPIO.RISING, callback=botao_pedestre_semaforo_principal, bouncetime=300)
    GPIO.add_event_detect(cruzamento_2['Pedestre_auxiliar'], GPIO.RISING, callback=botao_pedestre_semaforo_auxiliar, bouncetime=300)

    GPIO.add_event_detect(cruzamento_1['Passagem_1'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)
    GPIO.add_event_detect(cruzamento_1['Passagem_2'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)
    GPIO.add_event_detect(cruzamento_2['Passagem_1'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)
    GPIO.add_event_detect(cruzamento_2['Passagem_2'], GPIO.BOTH, callback=sensor_passagem_semaforo_auxiliar)

    GPIO.add_event_detect(cruzamento_1['Velocidade_1_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)
    GPIO.add_event_detect(cruzamento_1['Velocidade_2_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)
    GPIO.add_event_detect(cruzamento_2['Velocidade_1_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)
    GPIO.add_event_detect(cruzamento_2['Velocidade_2_A'], GPIO.BOTH, callback=sensor_parada_semaforo_principal)

    GPIO.add_event_detect(cruzamento_1['Velocidade_1_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)
    GPIO.add_event_detect(cruzamento_1['Velocidade_2_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)
    GPIO.add_event_detect(cruzamento_2['Velocidade_1_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)
    GPIO.add_event_detect(cruzamento_2['Velocidade_2_B'], GPIO.BOTH, callback=sensor_velocidade_semaforo_principal)


    rotina_semaforo(cruzamento_1)

    # thread_cruzamento_1 = Thread(target=rotina_semaforo, args=(cruzamento_1,))
    # thread_cruzamento_1.start()

    # thread_cruzamento_2 = Thread(target=rotina_semaforo, args=(cruzamento_2,))
    # thread_cruzamento_2.start()

    # thread_pedestre_1 = multiprocessing.Process(target=botao_pedestre_principal)
    # thread_pedestre_1.start()

    # thread_pedestre_2 = multiprocessing.Process(target=botao_pedestre_auxiliar)
    # thread_pedestre_2.start()

except KeyboardInterrupt:
    print("Saindo...")
    sys.exit()
