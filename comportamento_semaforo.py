import RPi.GPIO as GPIO
from time import sleep


def lista_cruzamento(cruzamento):
    return [cruzamento['Verde_principal'],
            cruzamento['Amarelo_principal'],
            cruzamento['Vermelho_principal'],
            cruzamento['Verde_auxiliar'],
            cruzamento['Amarelo_auxiliar'],
            cruzamento['Vermelho_auxiliar']]


def todos_vermelho(cruzamento):
    GPIO.output(lista_cruzamento(cruzamento), GPIO.LOW)
    GPIO.output(cruzamento['Vermelho_principal'], GPIO.HIGH)
    GPIO.output(cruzamento['Vermelho_auxiliar'], GPIO.HIGH)
    print("Todos vermelho")
    sleep(1)


def principal_verde(cruzamento):
    print("Principal verde")
    GPIO.output(lista_cruzamento(cruzamento), GPIO.LOW)
    GPIO.output(cruzamento['Verde_principal'], GPIO.HIGH)
    GPIO.output(cruzamento['Vermelho_auxiliar'], GPIO.HIGH)
    
        
def principal_amarelo(cruzamento):
    GPIO.output(lista_cruzamento(cruzamento), GPIO.LOW)
    GPIO.output(cruzamento['Amarelo_principal'], GPIO.HIGH)
    GPIO.output(cruzamento['Vermelho_auxiliar'], GPIO.HIGH)
    print("Principal amarelo")
    sleep(3)


def auxiliar_verde(cruzamento):
    print("Auxiliar verde")
    GPIO.output(lista_cruzamento(cruzamento), GPIO.LOW)
    GPIO.output(cruzamento['Vermelho_principal'], GPIO.HIGH)
    GPIO.output(cruzamento['Verde_auxiliar'], GPIO.HIGH)


def auxiliar_amarelo(cruzamento):
    GPIO.output(lista_cruzamento(cruzamento), GPIO.LOW)
    GPIO.output(cruzamento['Vermelho_principal'], GPIO.HIGH)
    GPIO.output(cruzamento['Amarelo_auxiliar'], GPIO.HIGH)
    print("Auxiliar amarelo")
    sleep(3)