import socket
import threading
import random
import json

# Connection Data
host = '127.0.0.1'
port = 55546

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# {'jogador0': '', 'nickjogador0': '', simbJogador0: 0 'jogador1': '', 'nickjogador1': '', simbJogador1: 0, 'ID': 0},
salas = []
IDCriados = []
simbolo = ['X', 'O']
board = [['', '', ''],
         ['', '', ''],
         ['', '', ''],]

def checkWin(linha, coluna):
    return False

def checkVelha(linha, coluna):
    return False

def resetGame():
    board = [['', '', ''],
             ['', '', ''],
             ['', '', ''],]

def endGame():
    board = [['', '', ''],
             ['', '', ''],
             ['', '', ''],]

# Handling Messages From Clients
def handle(sala):
    # Avidar o jogador q criou a sala (sempre o jogador0) que alguem entrou na sala dele 
    sala['jogador0'].send('START'.encode('ascii'))

    movimento = ""

    # pegar qual dos clientes vao jogar primeiro
    jogando = random.randint(0, 1)
    oponente = 1 - jogando

    sala['simbJogador0'] = jogando        
    sala['simbJogador1'] = oponente

    sala['jogador' + str(jogando)].send(str(jogando).encode('ascii'))
    sala['jogador' + str(oponente)].send(str(oponente).encode('ascii'))
    
    while True:

        sala['jogador' + str(jogando)].send('PLAY'.encode('ascii'))
        sala['jogador' + str(oponente)].send('WAIT'.encode('ascii'))
        
        while True:
            movimento = int(sala['jogador' + str(jogando)].recv(2).decode('ascii'))
            linha = int(movimento // 10)
            coluna = int(movimento % 10)

            if(board[linha][coluna] == ''):
                board[linha][coluna] = simbolo[jogando]
                break
            else:
                sala['jogador' + str(jogando)].send('INV'.encode('ascii'))
        
        win = checkWin(linha, coluna)
        velha = checkVelha(linha, coluna)

        if win == True:
            sala['jogador' + str(jogando)].send('WIN'.encode('ascii'))
            sala['jogador' + str(oponente)].send('DEF'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
        elif velha == True:
            sala['jogador' + str(jogando)].send('TIE'.encode('ascii'))
            sala['jogador' + str(oponente)].send('TIE'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
        else:
            sala['jogador' + str(jogando)].send('VAL'.encode('ascii'))
            sala['jogador' + str(oponente)].send('VAL'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
            

        if win or velha:
            continuar1 = int(sala['jogador' + str(jogando)].recv(9).decode('ascii'))
            continuar2 = int(sala['jogador' + str(oponente)].recv(9).decode('ascii'))
            
            if continuar1 == "CONTINUAR" and continuar2 == "CONTINUAR":    
                sala['jogador' + str(jogando)].send('CONTINUAR'.encode('ascii'))
                sala['jogador' + str(oponente)].send('CONTINUAR'.encode('ascii'))
                resetGame()
            else:
                sala['jogador' + str(jogando)].send('END'.encode('ascii'))
                sala['jogador' + str(oponente)].send('END'.encode('ascii'))
                endGame(sala)
                break

        jogando = 1 - jogando
        oponente = 1 - oponente        

def joinRoom(client, address):
    print("CONNECTED JOIN{}".format(str(address)))

    while True:
        client.send('IDRQ'.encode('ascii'))
        ID = client.recv(8).decode('ascii')
        print("ID RECEBIDO: " + ID)
        if next((sala for sala in salas if sala['ID'] == ID), None) != None : break

    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    print("NICK RECEBIDO: " + nickname)

    salaCompleta = {}
    for sala in salas:
        if sala['ID'] == ID:
            sala['jogador1'] = client
            sala['nickjogador1'] = nickname
            salaCompleta = sala
            break
    
    print("SALA COMPLETA")
    print("{")
    [print(key,':',value) for key, value in salaCompleta.items()]
    print("}")

    thread = threading.Thread(target=handle, args=(salaCompleta,))
    thread.start()

def createRoom(client, address):
    print("CONNECTED CREATE {}".format(str(address)))

    ID = str(random.randint(10000000, 99999999))
    while ID in IDCriados:
        ID = str(random.randint(10000000, 99999999))
    client.send(ID.encode('ascii')) # 8 bytes
    print("ID CRIADO: " + ID)

    client.send('NICK'.encode('ascii')) # 4 bytes
    nickname = client.recv(1024).decode('ascii') # Nick = 1024 Bytes
    print("NICK RECEBIDO: " + nickname)

    salas.append({'jogador0': client, 'nickjogador0': nickname, 'ID': ID})

    print("SALA CRIADA")
    print("{")
    [print(key,':',value) for key, value in salas[salas.__len__()-1].items()]
    print("}")


def decide():
    while True:
        print("\nSERVIDOR ESPERANDO\n")
        client, address = server.accept()

        escolha = client.recv(1024).decode('ascii')

        if escolha == "JOIN":
            joinRoom(client, address)
        elif escolha == "CREATE":
            createRoom(client, address)

decide()