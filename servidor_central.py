import socket
from _thread import *
from threading import Thread
import json
import sys

HOST = sys.argv[-1]
PORT = 10191
server_socket = socket.socket()

server_socket.bind((HOST, PORT))
server_socket.listen(5)

lista_address = []

def recebe_dados_client(conn):
    conn.send(str.encode('Entrou no servidor central'))
    while True:
        b = b''
        if not conn.recv(1024):
            break
        b += conn.recv(1024)
        dados = json.loads(b.decode('utf-8'))
        print(conn.getpeername())
        print(f"CRUZAMENTO {dados['Cruzamento']}:")
        print(f"Numero de carros por minuto na via principal: {dados['Numero_veiculos']/(dados['Temporizador'] / 60)} carros/min")
        print(f"Numero de infracoes de avancos no sinal vermelho: {dados['Avanco_sinal_vermelho']}")
        print(f"Numero de infracoes de velocidade acima do limite: {dados['Acima_velocidade_limite']}")
        print(f"Velocidade media da via principal: {sum(dados['Media_velocidade'])/len(dados['Media_velocidade'])} Km/h")
        print(f"=========================================================")
    conn.close()

def envia_dados_client():
    
    while True:        
        msg = input('Digite a opcao: ')

        if msg == '5':
            for addr in lista_address:
                addr.sendall(str.encode(msg))
        elif msg == '6':
            for addr in lista_address:
                addr.sendall(str.encode(msg))
        elif msg == '1':
            if len(lista_address) >= 1:
                lista_address[0].sendall(str.encode(msg))
            if len(lista_address) >= 2:
                lista_address[1].sendall(str.encode(msg))
        elif msg == '2':
            if len(lista_address) >= 1:
                lista_address[0].sendall(str.encode(msg))
            if len(lista_address) >= 2:
                lista_address[1].sendall(str.encode(msg))  
        elif msg == '3':
            if len(lista_address) >= 3:
                lista_address[2].sendall(str.encode(msg))
            if len(lista_address) >= 4:
                lista_address[3].sendall(str.encode(msg))
        elif msg == '4':
            if len(lista_address) >= 3:
                lista_address[2].sendall(str.encode(msg))
            if len(lista_address) >= 4:
                lista_address[3].sendall(str.encode(msg))


try:
    cont = 0
    print('''Opcoes:
        1 - Ligar modo de emergencia nos cruzamentos 1 e 2
        2 - Desligar modo de emergencia nos cruzamentos 1 e 2
        3 - Ligar modo de emergencia nos cruzamentos 3 e 4
        4 - Desligar modo de emergencia nos cruzamentos 3 e 4
        5 - Ligar modo noturno
        6 - Desligar modo noturno''')
    while True:
        conn, addr = server_socket.accept()
        lista_address.append(conn)
        print('\nConexão realizada por:', addr[0] + ':' + str(addr[1]))
        start_new_thread(recebe_dados_client, (conn,))
        thread_envia_dados = Thread(target=envia_dados_client)
        thread_envia_dados.start()

except KeyboardInterrupt:
    server_socket.close()
    print('\nServidor Central encerrado')
    exit()
