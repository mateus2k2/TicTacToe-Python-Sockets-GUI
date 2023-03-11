import socket
import threading
import random
from IA import IAOponent
import time

# Connection Data
host = '127.0.0.1'
port = 55553
limiteSalas = 10

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

#------------------------------------------------------------------------------------------------------------------------------------------------------

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
    salas.remove(sala)

#------------------------------------------------------------------------------------------------------------------------------------------------------

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
    jogador1.send(str(movimento).encode('ascii'))
    jogador2.send(str(movimento).encode('ascii'))
    
def handle(sala):
    try:
        play(sala)
    # Caso  tenha algum erro no jogo, o servidor encerra a sala
    except:
        print("Client Saiu")   
        endGame(sala)

def play(sala):
    # ---------------------------------------------------------------
    # Avidar o jogador q criou a sala (sempre o jogador0) que alguem entrou na sala dele 
    sala['jogador0'].send('START'.encode('ascii'))

    # ---------------------------------------------------------------
    # Inicializa o jogo
    # sala['board'] = [[ '', 'O', 'X'], 
    #                  ['X', 'O', 'X'],
    #                  ['O', 'X', 'O'],]
    # sala['jogadas'] = 8 
    
    sala['board'] =[['', '', ''],
                    ['', '', ''],
                    ['', '', ''],]
    sala['jogadas'] = 0 
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
    
    # Envia o nick de cada jogador
    sala['jogador' + str(jogando)].send(sala['nickjogador' + str(oponente)].encode('ascii'))
    sala['jogador' + str(oponente)].send(sala['nickjogador' + str(jogando)].encode('ascii'))
    
    while True:

        # ---------------------------------------------------------------
        # Envia Qual o turno de cada jogador

        sala['jogador' + str(jogando)].send('PLAY'.encode('ascii'))
        sala['jogador' + str(oponente)].send('WAIT'.encode('ascii'))
        
        # ---------------------------------------------------------------
        # Recebe o movimento do jogador

        movimento = int(sala['jogador' + str(jogando)].recv(2).decode('ascii'))
        linha = int(movimento // 10) - 1
        coluna = int(movimento % 10) - 1

        if(sala['board'][linha][coluna] == ''):
            sala['board'][linha][coluna] = simbolo[sala['simbJogador' + str(jogando)]]
            sala['jogadas'] += 1
        else:
            sala['jogador' + str(jogando)].send('INV'.encode('ascii'))
            sala['jogador' + str(oponente)].send('INV'.encode('ascii'))
        
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

def handleIA(sala):
    try:
        playIA(sala)
    # Caso  tenha algum erro no jogo, o servidor encerra a sala
    except:
        print("Client Saiu")   
        sala['jogador0'].close()
        
def playIA(sala):
    # ---------------------------------------------------------------
    sala['board'] =[['', '', ''],
                    ['', '', ''],
                    ['', '', ''],]
    sala['jogadas'] = 0 
    movimento = ""
    
    IAObj = IAOponent()
        
    # ---------------------------------------------------------------
    theFirstPlayerNumber  = random.randint(0, 1) # 0 Jogador 1 Maquina
    turnoDeQuem = theFirstPlayerNumber
    
    # ---------------------------------------------------------------
    # Envia o simbolo de cada jogador X (Quem começa) e O (Quem espera)
    sala['simbJogador0'] = theFirstPlayerNumber        
    sala['simbMaquina'] = 1 - theFirstPlayerNumber       
    
    sala['jogador0'].send(str(theFirstPlayerNumber).encode('ascii'))
        
    sala['jogador0'].send("Maquina------------------".encode('ascii'))
    
    while True:

        # ---------------------------------------------------------------
        # Envia Qual o turno de cada jogador

        if turnoDeQuem == 0: sala['jogador0'].send('PLAY'.encode('ascii'))
        if turnoDeQuem == 1: sala['jogador0'].send('WAIT'.encode('ascii'))
        
        # ---------------------------------------------------------------
        # Recebe o movimento do jogador
        
        if turnoDeQuem == 0:
            movimento = int(sala['jogador0'].recv(2).decode('ascii'))
            linha = int(movimento // 10) - 1
            coluna = int(movimento % 10) - 1

            if(sala['board'][linha][coluna] == ''):
                sala['board'][linha][coluna] = simbolo[sala['simbJogador0']]
                sala['jogadas'] += 1
            else:
                sala['jogador0'].send('INV'.encode('ascii'))
        
        if turnoDeQuem == 1:
            time.sleep(5)
            #boardMatrix, computerletter, theFirstPlayerNumber, turnNumber, difficulty
            movimento = int(IAObj.getComputerMove(sala['board'], sala['simbMaquina'], theFirstPlayerNumber, sala['jogadas'], sala['dificuldade']))         

            linha = int(movimento // 10) - 1
            coluna = int(movimento % 10) - 1

            sala['board'][linha][coluna] = simbolo[sala['simbMaquina']]
            sala['jogadas'] += 1
        
        # ---------------------------------------------------------------
        # Verifica se o jogo acabou

        win = checkWin(sala)
        velha = checkVelha(sala)

        # ---------------------------------------------------------------
        # Envia o estado do jogo para os jogadores

        if win == True and turnoDeQuem == 0:
            sala['jogador0'].send('WIN'.encode('ascii')) 
            sala['jogador0'].send(str(movimento).encode('ascii'))
        elif win == True and turnoDeQuem == 1:
            sala['jogador0'].send('DEF'.encode('ascii')) 
            sala['jogador0'].send(str(movimento).encode('ascii'))
        elif velha == True:
            sala['jogador0'].send('TIE'.encode('ascii')) 
            sala['jogador0'].send(str(movimento).encode('ascii'))
        else:
            sala['jogador0'].send('VAL'.encode('ascii')) 
            sala['jogador0'].send(str(movimento).encode('ascii'))

        # ---------------------------------------------------------------
        # Verificar se os dois jogadores querem continuar jogando depois de dar velha ou ganhar

        if win or velha:
            continuar1 = sala['jogador0'].recv(3).decode('ascii')

            if continuar1 == "CNT":  
                sala['jogador0'].send('CNT'.encode('ascii'))
                resetGame(sala)
                
            elif continuar1 == "END":
                sala['jogador0'].send('END'.encode('ascii'))
                sala['jogador0'].close()
                salas.remove(sala)
                break
        
        # ---------------------------------------------------------------
        # Troca de turno
        turnoDeQuem = 1 - turnoDeQuem

#------------------------------------------------------------------------------------------------------------------------------------------------------

def joinRoom(client, address):
    print("CONNECTED JOIN{}".format(str(address)))

    client.send('NICK'.encode('ascii')) # Envia Requisição de nickname
    nickname = client.recv(25).decode('ascii') # Recebe o nickname
    print("NICK RECV: " + nickname)
    
    salaCompleta = {}
    while True:
        client.send('IDRQ'.encode('ascii')) # Envia Requisição de ID
        ID = client.recv(8).decode('ascii') # Recebe o ID
        print("ID RECV: " + ID)
        
        if(not (ID == '--RAND--')):
            salaCompleta = next((sala for sala in salas if sala['ID'] == ID), None) # Procura a sala com o ID
            if salaCompleta != None and (not ('jogador1' in salaCompleta)): # Se a sala existe e não está completa
                client.send('IDOK'.encode('ascii')) # Envia confirmação de ID
                break # Sai do loop
        
        if(ID == '--RAND--'):
            salaCompleta = next((sala for sala in salas if (not ('jogador1' in sala) and ('jogador0' in sala))), None)
            if salaCompleta != None: # Se a sala existe e não está completa
                client.send('IDOK'.encode('ascii')) # Envia confirmação de ID
                break # Sai do loop
            
        client.send('IDRQ'.encode('ascii')) # Se não envia mais Requisição de ID

    salaCompleta['jogador1'] = client # Adiciona o client do jogador na sala
    salaCompleta['nickjogador1'] = nickname # Adiciona o nickname do jogador 1 na sala
    
    print("\nSALA COMPLETA")
    [print(key,':',str(value)[:50]) for key, value in salaCompleta.items()]

    handle(salaCompleta)

def createRoom(client, address):
    print("CONNECTED CREATE {}".format(str(address)))

    ID = str(random.randint(10000000, 99999999)) # Gera um ID aleatório de 8 dígitos
    while ID in IDCriados: # Verifica se o ID já foi criado
        ID = str(random.randint(10000000, 99999999)) # Se sim, gera outro
    client.send(ID.encode('ascii')) # Envia o ID
    print("ID CRIADO: " + ID)

    client.send('NICK'.encode('ascii')) # Envia Requisição de nickname
    nickname = client.recv(25).decode('ascii') # Recebe o nickname
    print("NICK RECEBIDO: " + nickname)
    
    # Cria uma novo item no vetor de dicionario de salas com o client do jogador 0 o nickname do jogador e o ID
    salas.append({'jogador0': client, 'nickjogador0': nickname, 'ID': ID}) 

    print("\nSALA CRIADA")
    [print(key,':',str(value)[:50]) for key, value in salas[salas.__len__()-1].items()]

def joinRoomIA(client, address):
    print("CONNECTED CREATE {}".format(str(address)))

    client.send('NICK'.encode('ascii')) # Envia Requisição de nickname
    nickname = client.recv(25).decode('ascii') # Recebe o nickname
    print("NICK RECEBIDO: " + nickname)

    client.send('DIFC'.encode('ascii')) # Envia Requisição de nickname
    dificuldade = int(client.recv(1).decode('ascii')) # Recebe o nickname
    print("DIFC RECEBIDO: " + str(dificuldade))
        
    # Cria uma novo item no vetor de dicionario de salas com o client do jogador 0 o nickname do jogador e o ID
    salas.append({'jogador0': client, 'nickjogador0': nickname, 'dificuldade': int(dificuldade)}) 

    print("\nSALA CRIADA")
    [print(key,':',str(value)[:50]) for key, value in salas[salas.__len__()-1].items()]

    handleIA(salas[salas.__len__()-1])

def decide():
    while True:
        print("---------------------------------------------------")
        print("SERVIDOR ESPERANDO\n")

        client, address = server.accept() # Aceita conexão

        if(salas.__len__() + 1 > limiteSalas): # Verifica se o limite de salas foi atingido
            client.send('FULL'.encode('ascii')) # Envia mensagem de servidor cheio
            client.close() # Fecha a conexão
        else:
            client.send('OK'.encode('ascii')) # Envia mensagem de servidor OK
        
        escolha = client.recv(6).decode('ascii') # Recebe a escolha do cliente
        
        if escolha == "JOIN": 
            print("JOIN")
            thread = threading.Thread(target=joinRoom, args=(client, address,))
            thread.start()
        
        elif escolha == "CREATE":
            print("CREATE")
            thread = threading.Thread(target=createRoom, args=(client, address,))
            thread.start()
            
        elif escolha == "JOINIA": 
            print("JOINIA")
            thread = threading.Thread(target=joinRoomIA, args=(client, address,))
            thread.start()

decide()