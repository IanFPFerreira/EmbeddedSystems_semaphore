import socket
from _thread import *
from threading import Thread
import json
from time import sleep
import sys
import os

HOST = sys.argv[-1]
PORT = 10191
server_socket = socket.socket()

server_socket.bind((HOST, PORT))
server_socket.listen(5)

lista_address = []
dict_dados = {
    'Cruzamento 1': {'Cruzamento': 1, 'Avanco_sinal_vermelho' : 0, 'Acima_velocidade_limite' : 0, 'Media_velocidade' : [0], 'Numero_veiculos' : 0, 'Temporizador' : 0.1},
    'Cruzamento 2': {'Cruzamento': 2, 'Avanco_sinal_vermelho' : 0, 'Acima_velocidade_limite' : 0, 'Media_velocidade' : [0], 'Numero_veiculos' : 0, 'Temporizador' : 0.1},
    'Cruzamento 3': {'Cruzamento': 3, 'Avanco_sinal_vermelho' : 0, 'Acima_velocidade_limite' : 0, 'Media_velocidade' : [0], 'Numero_veiculos' : 0, 'Temporizador' : 0.1},
    'Cruzamento 4': {'Cruzamento': 4, 'Avanco_sinal_vermelho' : 0, 'Acima_velocidade_limite' : 0, 'Media_velocidade' : [0], 'Numero_veiculos' : 0, 'Temporizador' : 0.1}
}

dict_cruzamentos = {
    'cruzamento_1': False,
    'cruzamento_2': False,
    'cruzamento_3': False,
    'cruzamento_4': False
}

tecla_pressionada = False

def recebe_dados_client(conn):
    '''Funcao que recebe os dados dos clientes'''
    global dict_dados
    conn.send(str.encode('Entrou no servidor central'))
    while True:
        b = b''
        if not conn.recv(1024):
            break
        b += conn.recv(1024)
        dados = json.loads(b.decode('utf-8'))
        if dados['Cruzamento'] == 1:
            dict_dados['Cruzamento 1'] = dados
        elif dados['Cruzamento'] == 2:
            dict_dados['Cruzamento 2'] = dados
        elif dados['Cruzamento'] == 3:
            dict_dados['Cruzamento 3'] = dados
        elif dados['Cruzamento'] == 4:
            dict_dados['Cruzamento 4'] = dados
    conn.close()

def envia_dados_client():
    '''Funcao que envia os dados para os clientes'''
    while True:
        print('''Opcoes:
        1 - Ligar modo de emergencia nos cruzamentos 1 e 2
        2 - Desligar modo de emergencia nos cruzamentos 1 e 2
        3 - Ligar modo de emergencia nos cruzamentos 3 e 4
        4 - Desligar modo de emergencia nos cruzamentos 3 e 4
        5 - Ligar modo noturno
        6 - Desligar modo noturno
        7 - Mostrar dados dos cruzamentos''')        
        msg = input('Digite a opcao: ')

        if msg == '5':
            for addr in lista_address:
                addr.sendall(str.encode(msg))
        elif msg == '6':
            for addr in lista_address:
                addr.sendall(str.encode(msg))
        elif msg == '1':
            if dict_cruzamentos['cruzamento_1']:
                dict_cruzamentos['cruzamento_1'].sendall(str.encode(msg))
            if dict_cruzamentos['cruzamento_2']:
                dict_cruzamentos['cruzamento_2'].sendall(str.encode(msg))
        elif msg == '2':
            if dict_cruzamentos['cruzamento_1']:
                dict_cruzamentos['cruzamento_1'].sendall(str.encode(msg))
            if dict_cruzamentos['cruzamento_2']:
                dict_cruzamentos['cruzamento_2'].sendall(str.encode(msg))  
        elif msg == '3':
            if dict_cruzamentos['cruzamento_3']:
                dict_cruzamentos['cruzamento_3'].sendall(str.encode(msg))
            if dict_cruzamentos['cruzamento_4']:
                dict_cruzamentos['cruzamento_4'].sendall(str.encode(msg))
        elif msg == '4':
            if dict_cruzamentos['cruzamento_3']:
                dict_cruzamentos['cruzamento_3'].sendall(str.encode(msg))
            if dict_cruzamentos['cruzamento_4']:
                dict_cruzamentos['cruzamento_4'].sendall(str.encode(msg))
        elif msg == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            mostra_dados_client()
        os.system('cls' if os.name == 'nt' else 'clear')


def verifica_tecla(s):
    '''Funcao que verifica se a tecla foi pressionada'''
    global tecla_pressionada
    while True:
        if input() == '0':
            tecla_pressionada = True
            break

def mostra_dados_client():
    '''Funcao que mostra os dados dos cruzamentos'''
    global dict_dados, tecla_pressionada
    d = start_new_thread(verifica_tecla, ('',))
    print(d)
    while not tecla_pressionada:
        for infos in dict_dados.values():
            print(f"CRUZAMENTO {infos['Cruzamento']}:")
            print(f"Numero de carros por minuto na via principal: {infos['Numero_veiculos']/(infos['Temporizador'] / 60)} carros/min")
            print(f"Numero de infracoes de avancos no sinal vermelho: {infos['Avanco_sinal_vermelho']}")
            print(f"Numero de infracoes de velocidade acima do limite: {infos['Acima_velocidade_limite']}")
            print(f"Velocidade media da via principal: {sum(infos['Media_velocidade'])/len(infos['Media_velocidade'])} Km/h")
            print(f"=========================================================")
        print('Digite 0 para voltar ao menu, pode demorar um instante!')
        sleep(6)
        os.system('cls' if os.name == 'nt' else 'clear')
    tecla_pressionada = False
        
try:
    print('Servidor central iniciado!')
    thread_envia_dados = Thread(target=envia_dados_client) # Thread que envia os dados para os clientes
    thread_envia_dados.start()
    while True:
        conn, addr = server_socket.accept()
        lista_address.append(conn)
        print('\nConexão realizada por:', addr[0] + ':' + str(addr[1]))
        dict_cruzamentos[conn.recv(1024).decode('utf-8')] = conn
        start_new_thread(recebe_dados_client, (conn,)) # Thread que recebe os dados dos clientes
except KeyboardInterrupt:
    print('\nServidor encerrado')
    server_socket.close()
    exit()
