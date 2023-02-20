import socket
import threading
import random

# Connection Data
host = '127.0.0.1'
port = 55546

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

salas = []
IDCriados = []
simbolo = ['X', 'O']

def checkWin(sala):
    for linha in range(3):
        if sala['board'][linha][0] == sala['board'][linha][1] == sala['board'][linha][2] != '':
            return True
    for col in range(3):
        if sala['board'][0][col] == sala['board'][1][col] == sala['board'][2][col] != '':
            return True
    for diag in range(2):
        if sala['board'][0][0] == sala['board'][1][1] == sala['board'][2][2] != '':
            return True
        elif sala['board'][0][2] == sala['board'][1][1] == sala['board'][2][0] != '':
            return True

def checkVelha(sala):
    return sala['jogadas'] == 9

def resetGame(sala):
    sala['board'][0][0] = ''; sala['board'][0][1] = ''; sala['board'][0][2]  = '';
    sala['board'][1][0] = ''; sala['board'][1][1] = ''; sala['board'][1][2]  = '';
    sala['board'][2][0] = ''; sala['board'][2][1] = ''; sala['board'][2][2]  = '';

    sala['jogadas'] = 0

def endGame(sala):
    sala['board'][0][0] = ''; sala['board'][0][1] = ''; sala['board'][0][2]  = '';
    sala['board'][1][0] = ''; sala['board'][1][1] = ''; sala['board'][1][2]  = '';
    sala['board'][2][0] = ''; sala['board'][2][1] = ''; sala['board'][2][2]  = '';

    sala['jogador0'].close()
    sala['jogador1'].close()

    # deletar a sala do vetor de salas
    # del next((salaRet for salaRet in salas if salaRet['ID'] == sala['ID']), None)
    salas.remove(sala)

def printBoard(sala):
    for row in sala['board']:
        for item in row:
            print(item, end=" ")
        print()

def handle(sala):
    # Avidar o jogador q criou a sala (sempre o jogador0) que alguem entrou na sala dele 
    sala['jogador0'].send('START'.encode('ascii'))
    sala['board'] = [[ '', 'O', 'X'], #--------------------------------------
                     ['X', 'O', 'X'],
                     ['O', 'X', 'O'],]
    sala['jogadas'] = 8 #------------------------------------------------
    movimento = ""

    # pegar qual dos clientes vao jogar primeiro
    jogando = random.randint(0, 1)
    oponente = 1 - jogando

    sala['simbJogador0'] = jogando        
    sala['simbJogador1'] = oponente

    sala['jogador' + str(jogando)].send("0".encode('ascii'))
    sala['jogador' + str(oponente)].send("1".encode('ascii'))
    
    while True:

        sala['jogador' + str(jogando)].send('PLAY'.encode('ascii'))
        sala['jogador' + str(oponente)].send('WAIT'.encode('ascii'))
        
        while True:
            movimento = int(sala['jogador' + str(jogando)].recv(2).decode('ascii'))
            linha = int(movimento // 10) - 1
            coluna = int(movimento % 10) - 1

            if(sala['board'][linha][coluna] == ''):
                sala['board'][linha][coluna] = simbolo[jogando]
                sala['jogadas'] += 1
                break
            else:
                sala['jogador' + str(jogando)].send('INV'.encode('ascii'))
        
        win = checkWin(sala)
        velha = checkVelha(sala)

        if win == True:
            sala['jogador' + str(jogando)].send('WIN'.encode('ascii'))
            sala['jogador' + str(oponente)].send('DEF'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))

            # printBoard(sala)
        elif velha == True:
            sala['jogador' + str(jogando)].send('TIE'.encode('ascii'))
            sala['jogador' + str(oponente)].send('TIE'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
            
            # printBoard(sala)
        else:
            sala['jogador' + str(jogando)].send('VAL'.encode('ascii'))
            sala['jogador' + str(oponente)].send('VAL'.encode('ascii'))
            sala['jogador' + str(jogando)].send(str(movimento).encode('ascii'))
            sala['jogador' + str(oponente)].send(str(movimento).encode('ascii'))
            
            # printBoard(sala)
            

        if win or velha:
            continuar1 = sala['jogador' + str(jogando)].recv(3).decode('ascii')
            continuar2 = sala['jogador' + str(oponente)].recv(3).decode('ascii')

            if continuar1 == "CNT" and continuar2 == "CNT":  
                print("Resetando jogo")
                sala['jogador' + str(jogando)].send('CNT'.encode('ascii'))
                sala['jogador' + str(oponente)].send('CNT'.encode('ascii'))
                resetGame(sala)
            elif continuar1 == "END" and continuar2 == "END":
                print("Encerrando o jogo")
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