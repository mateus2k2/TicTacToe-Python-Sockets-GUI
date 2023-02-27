import socket

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# inicializa o jogo
ID = ""
nickname = ""
nicknameOpodente = ""
board = [['', 'O', 'X'],
         ['X', 'O', 'X'],
         ['O', 'X', 'O'],]
# board = [['', '', ''],
#          ['', '', ''],
#          ['', '', ''],]

# vetor auxiliar para determinar o simbolo do jogador
simbolos = ['X', 'O']

def printBoard():
    for i in range(3):
        print("-" * 14)
        print("|", end=" ")
        for j in range(3):
            elem = ''
            if(board[i][j] == ''): elem = ' ' 
            else: elem = board[i][j]
            print(elem, "|", end=" ")
        print()
    print("-" * 14)

def resetGame():
    board[0][0] = ''; board[0][1] = ''; board[0][2]  = '';
    board[1][0] = ''; board[1][1] = ''; board[1][2]  = '';
    board[2][0] = ''; board[2][1] = ''; board[2][2]  = '';

def endGame():
    board[0][0] = ''; board[0][1] = ''; board[0][2]  = '';
    board[1][0] = ''; board[1][1] = ''; board[1][2]  = '';
    board[2][0] = ''; board[2][1] = ''; board[2][2]  = '';
    client.close()

def recvGameState(simbolo):
    movimento = int(client.recv(2).decode('ascii'))
    linha = int(movimento // 10) - 1
    coluna = int(movimento % 10) - 1
    board[linha][coluna] = simbolos[simbolo]
    
    returno = -1
    if movimento == 11: returno = 0 
    if movimento == 12: returno = 1 
    if movimento == 13: returno = 2 
    if movimento == 21: returno = 3 
    if movimento == 22: returno = 4 
    if movimento == 23: returno = 5 
    if movimento == 31: returno = 6 
    if movimento == 32: returno = 7 
    if movimento == 33: returno = 8 

    print("MOVIMENTO: " + str(movimento))

    return returno

def endGameDecide(response, event, fileResultado):
    if response == True:
        continuar = 'CNT'
    else:
        continuar = 'END'
    client.send(continuar.encode('ascii'))

    if continuar == "END":
        print("FIM JOGO")
        event.set()
        fileResultado.put(True)
        return True
    
    print("ESPERANDO RESPOSTA SERVER")
    continuar = client.recv(3).decode('ascii')

    if continuar == "CNT":
        print("RESET GAME")
        event.set()
        fileResultado.put(False)
        return False

def getSimbolo():
    simbolo = int(client.recv(1).decode('ascii'))
    print("SIMBOLO: " + simbolos[simbolo]); print()
    return simbolo

def continuar(continuar):
    # continuar = "CNT" #input("Escolha CNT ou END: ")
    client.send(continuar.encode('ascii'))

    if continuar == "END":
        print("FIM JOGO")
        return False

    print("ESPERANDO RESPOSTA SERVER")
    continuar = client.recv(3).decode('ascii')

    if continuar == "END":
        print("OUTRO JOGADOR DESISTIU")
        return False

    print("CONTINUAR: " + continuar)
    return True

def getTurn():
    message = client.recv(4).decode('ascii')
    print("MENSAGEM: " + message)
    return message

def sendMove(movimentoGUI):
    client.send(movimentoGUI.encode('ascii'))
    message = client.recv(3).decode('ascii'); print("MENSAGEM: " + message)
    return message

def waitResponse(event, fileResultado):
    message = client.recv(3).decode('ascii')
    fileResultado.put(message)
    event.set()
    return message

def connectToServer(ip, port):
    try:
        client.connect((ip, port))
    except:
        print("Server is not running")
        return False
    return True
    
def joinGame(GUINick):
    # if connectToServer('127.0.0.1', 55549) == False:
    #     return 'Server is not running'

    client.send("JOIN".encode('ascii'))
    print("JOIN")

    message = client.recv(4).decode('ascii')
    nickname = GUINick
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

def sendID(GUIID):
    # print("GUIID" + GUIID)
    # message = client.recv(4).decode('ascii')
    # print("MENSAGEM: " + message)
    # if message != "IDRQ": return True
    # ID = GUIID
    # client.send(ID.encode('ascii'))
    # return False

    message = client.recv(4).decode('ascii')
    ID = GUIID
    client.send(ID.encode('ascii'))
    print("MENSAGEM: " + message)
    message = client.recv(4).decode('ascii')
    if message != "IDRQ": return True
    return False

def createGame(GUINick):
    # if connectToServer('127.0.0.1', 55549) == False:
    #     return 'Server is not running'
        
    client.send("CREATE".encode('ascii'))
    print("CREATE")

    message = client.recv(8).decode('ascii')
    ID = message
    print("MENSAGEM: " + ID)

    # nickname = input("Input NICK: ")
    nickname = GUINick
    message = client.recv(4).decode('ascii')
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    return ID

def waitingRoom(event):
    print("WAINTING FOR PLAYER")
    message = client.recv(5).decode('ascii')
    print("MENSAGEM: " + message)
    if message == 'START': 
        event.set()
        return True
    return False

