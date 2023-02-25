import socket
import threading
import random

# Connection Data
host = '127.0.0.1'
port = 55599

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
    for i in range(3):
        print("-" * 14)
        print("|", end=" ")
        for j in range(3):
            elem = ''
            if(sala['board'][i][j] == ''): elem = ' ' 
            else: elem = sala['board'][i][j]
            print(elem, "|", end=" ")
        print()
    print("-" * 14)

def sendGameState(jogador1, jogador2,  mensagem1, mensagem2, movimento):
    jogador1.send(mensagem1.encode('ascii'))
    jogador2.send(mensagem2.encode('ascii'))
    jogador2.send(mensagem2.encode('ascii'))
    jogador1.send(str(movimento).encode('ascii'))
    jogador2.send(str(movimento).encode('ascii'))
    
def handle(sala):
    # ---------------------------------------------------------------
    # Avidar o jogador q criou a sala (sempre o jogador0) que alguem entrou na sala dele 
    sala['jogador0'].send('START'.encode('ascii'))

    # ---------------------------------------------------------------
    # Inicializa o jogo
    sala['board'] = [[ '', 'O', 'X'], 
                     ['X', 'O', 'X'],
                     ['O', 'X', 'O'],]
    sala['jogadas'] = 8 
    
    # sala['board'] =[['', '', ''],
    #                 ['', '', ''],
    #                 ['', '', ''],]
    # sala['jogadas'] = 0 
    movimento = ""

    # ---------------------------------------------------------------
    # Sorteia quem vai começar
    jogando = random.randint(0, 1)
    oponente = 1 - jogando

    # ---------------------------------------------------------------
    # Envia o simbolo de cada jogador X (Quem começa) e O (Quem espera)
    sala['simbJogador' + str(jogando)] = 0        
    sala['simbJogador' + str(oponente)] = 1

    sala['jogador' + str(jogando)].send("0".encode('ascii'))
    sala['jogador' + str(oponente)].send("1".encode('ascii'))
    
    while True:
        # ---------------------------------------------------------------
        # Verificar se os dois jogadores querem continuar jogando

        continuar1 = sala['jogador' + str(jogando)].recv(3).decode('ascii')
        continuar2 = sala['jogador' + str(oponente)].recv(3).decode('ascii')

        print("CONTINUAR1: " + continuar1)
        print("CONTINUAR2: " + continuar2)

        if continuar1 == "CNT" and continuar2 == "CNT":  
            sala['jogador' + str(jogando)].send('CNT'.encode('ascii'))
            sala['jogador' + str(oponente)].send('CNT'.encode('ascii'))
        elif continuar1 == "END" or continuar2 == "END":
            sala['jogador' + str(jogando)].send('END'.encode('ascii'))
            sala['jogador' + str(oponente)].send('END'.encode('ascii'))
            endGame(sala)
            break
        # ---------------------------------------------------------------
        # Envia Qual o turno de cada jogador

        sala['jogador' + str(jogando)].send('PLAY'.encode('ascii'))
        sala['jogador' + str(oponente)].send('WAIT'.encode('ascii'))
        
        # ---------------------------------------------------------------
        # Recebe o movimento do jogador

        while True:
            movimento = int(sala['jogador' + str(jogando)].recv(2).decode('ascii'))
            linha = int(movimento // 10) - 1
            coluna = int(movimento % 10) - 1

            if(sala['board'][linha][coluna] == ''):
                sala['board'][linha][coluna] = simbolo[sala['simbJogador' + str(jogando)]]
                sala['jogadas'] += 1
                break
            else:
                sala['jogador' + str(jogando)].send('INV'.encode('ascii'))
        
        # ---------------------------------------------------------------
        # Verifica se o jogo acabou

        win = checkWin(sala)
        velha = checkVelha(sala)

        # ---------------------------------------------------------------
        # Envia o estado do jogo para os jogadores

        if win == True:
            sendGameState(sala['jogador' + str(jogando)], sala['jogador' + str(oponente)], 'WIN', 'DEF', movimento)
            # printBoard(sala)
        elif velha == True:
            sendGameState(sala['jogador' + str(jogando)], sala['jogador' + str(oponente)], 'TIE', 'TIE', movimento)
            # printBoard(sala)
        else:
            sendGameState(sala['jogador' + str(jogando)], sala['jogador' + str(oponente)], 'VAL', 'VAL', movimento)
            # printBoard(sala)

        # ---------------------------------------------------------------
        # Verificar se os dois jogadores querem continuar jogando depois de dar velha ou ganhar

        if win or velha:
            continuar1 = sala['jogador' + str(jogando)].recv(3).decode('ascii')
            continuar2 = sala['jogador' + str(oponente)].recv(3).decode('ascii')

            if continuar1 == "CNT" and continuar2 == "CNT":  
                # print("\nRESET GAME")
                sala['jogador' + str(jogando)].send('CNT'.encode('ascii'))
                sala['jogador' + str(oponente)].send('CNT'.encode('ascii'))
                resetGame(sala)
            elif continuar1 == "END" or continuar2 == "END":
                # print("END GAME")
                sala['jogador' + str(jogando)].send('END'.encode('ascii'))
                sala['jogador' + str(oponente)].send('END'.encode('ascii'))
                endGame(sala)
                break
        
        # ---------------------------------------------------------------
        # Troca de turno

        jogando = 1 - jogando
        oponente = 1 - oponente        

def joinRoom(client, address):
    print("CONNECTED JOIN{}".format(str(address)))

    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    print("NICK RECV: " + nickname)
    
    while True:
        client.send('IDRQ'.encode('ascii'))
        ID = client.recv(8).decode('ascii')
        print("ID RECV: " + ID)
        if next((sala for sala in salas if sala['ID'] == ID), None) != None : 
            # Verificar se a sala encontrada ja tem o jogador1 ou não
            # se tiver retornar IDRQ  
            client.send('IDOK'.encode('ascii'))
            break
        client.send('IDRQ'.encode('ascii'))

    salaCompleta = {}
    for sala in salas:
        if sala['ID'] == ID:
            sala['jogador1'] = client
            sala['nickjogador1'] = nickname
            salaCompleta = sala
            break
    
    print("\nSALA COMPLETA")
    [print(key,':',str(value)[:50]) for key, value in salaCompleta.items()]

    handle(sala)

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

    print("\nSALA CRIADA")
    [print(key,':',str(value)[:50]) for key, value in salas[salas.__len__()-1].items()]


def decide():
    while True:
        print("---------------------------------------------------")
        print("SERVIDOR ESPERANDO\n")

        client, address = server.accept()

        escolha = client.recv(1024).decode('ascii')

        if escolha == "JOIN":
            thread = threading.Thread(target=joinRoom, args=(client, address,))
            thread.start()
        elif escolha == "CREATE":
            thread = threading.Thread(target=createRoom, args=(client, address,))
            thread.start()

decide()