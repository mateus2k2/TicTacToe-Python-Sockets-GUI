import socket
import threading
import random

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# {'jogador0': '', 'nickjogador0': '', 'jogador1': '', 'nickjogador1': '', 'ID': 0},
salas = []
IDCriados = []
simbolo = ['X', 'O']

board = [[]]

def checkWin(linha, coluna):
    pass

def checkVelha(linha, coluna):
    pass

def resetGame():
    pass

def endGame():
    pass

# Handling Messages From Clients
def handle(sala):
    movimento = ""

    jogando = random.randint(0, 1)
    oponente = 1 - jogando        
    while True:
        # pegar qual dos clientes vao jogar primeiro

        sala['jogador' + str(jogando)].send('TURN'.encode('ascii'))
        sala['jogador' + str(oponente)].send('WAIT'.encode('ascii'))

        movimento = int(sala['jogador' + str(jogando)].recv(1024).decode('ascii'))
        linha = int(movimento // 10)
        coluna = int(movimento % 10)

        if(board[linha][coluna] == ''):
            board[linha][coluna] = simbolo[jogando]
        else:
            sala['jogador' + str(jogando)].send('INVALID'.encode('ascii'))
        
        while board[linha][coluna] is not '':
            movimento = int(sala['jogador' + str(jogando)].recv(1024).decode('ascii'))
            linha = int(movimento // 10)
            coluna = int(movimento % 10)

            if(board[linha][coluna] == ''):
                board[linha][coluna] = simbolo[jogando]
            else:
                sala['jogador' + str(jogando)].send('INVALID'.encode('ascii'))

        win = checkWin(linha, coluna)
        velha = checkVelha(linha, coluna)

        if win == True:
            sala['jogador' + str(jogando)].send('WIN'.encode('ascii'))
            sala['jogador' + str(oponente)].send('LOOSE'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
        elif velha == True:
            sala['jogador' + str(jogando)].send('TIE'.encode('ascii'))
            sala['jogador' + str(oponente)].send('TIE'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
        else:
            sala['jogador' + str(jogando)].send('VALID'.encode('ascii'))
            sala['jogador' + str(oponente)].send('VALID'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
            

        if win or velha:
            continuar1 = int(sala['jogador' + str(jogando)].recv(1024).decode('ascii'))
            continuar2 = int(sala['jogador' + str(oponente)].recv(1024).decode('ascii'))
            
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
    print("CONNECTED {}".format(str(address)))

    client.send('IDREQUEST '.encode('ascii'))
    ID = client.recv(1024).decode('ascii')
    
    while next((sala for sala in salas if sala['ID'] == ID), None) == None:
        client.send('IDREQUEST '.encode('ascii'))
        ID = client.recv(1024).decode('ascii')

    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    
    salaCompleta = {}
    for sala in salas:
        if sala['ID'] == ID:
            sala['jogador1'] = client
            sala['nickjogador1'] = nickname
            salaCompleta = sala
            break

    print(salaCompleta)

    # Start Handling Thread For Client
    thread = threading.Thread(target=handle, args=(salaCompleta,))
    thread.start()

def createRoom(client, address):
    print("CONNECTED {}".format(str(address)))

    ID = str(random.randint(10000000, 99999999))
    while ID in IDCriados:
        ID = str(random.randint(10000000, 99999999))
    client.send('ID {}'.format(ID).encode('ascii'))

    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')

    salas.append({'jogador0': client, 'nickjogador0': nickname, 'ID': ID})

    print(salas[salas.__len__()-1])

    # verficar se a sala salas[salas.__len__()-1] tem mais um jogador
    while('jogador2' in [sala.keys() for sala in salas] == False): continue
    client.send('START'.encode('ascii'))


def decide():
    client, address = server.accept()

    escolha = client.recv(1024).decode('ascii')

    if escolha == "JOIN":
        joinRoom(client, address)
    elif escolha == "CREATE":
        createRoom(client, address)

decide()