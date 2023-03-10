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

    print("MOVIMENTO: " + str(movimento))

def endGameDecide():
    continuar = input("Escolha CNT ou END: ")
    client.send(continuar.encode('ascii'))

    if continuar == "END":
        print("FIM JOGO")
        endGame()
        return True
    
    print("ESPERANDO RESPOSTA SERVER")
    continuar = client.recv(3).decode('ascii')

    if continuar == "CNT":
        print("RESET GAME")
        resetGame()
        return False

def jogar():
    print("\nJOGANDO")
    movimento = ""

    simbolo = int(client.recv(1).decode('ascii'))
    print("SIMBOLO: " + simbolos[simbolo]); print()

    printBoard(); print()

    while True:
        print("---------------------------------------------------")

        # ---------------------------------------------------------------
        continuar = "CNT" #input("Escolha CNT ou END: ")
        client.send(continuar.encode('ascii'))

        if continuar == "END":
            print("FIM JOGO")
            endGame()
            break

        print("ESPERANDO RESPOSTA SERVER")
        continuar = client.recv(3).decode('ascii')

        if continuar == "END":
            print("OUTRO JOGADOR DESISTIU")
            endGame()
            break

        print("CNT")
        # ---------------------------------------------------------------

        message = client.recv(4).decode('ascii')
        print("MENSAGEM: " + message)
        
        if message == 'PLAY':

            while True:
                movimento = input("Digite o Movimento: ")
                client.send(movimento.encode('ascii'))
                message = client.recv(3).decode('ascii'); print("MENSAGEM: " + message)
                if message != "INV": break

            # message = client.recv(5).decode('ascii')
            if message == "WIN":
                print("WIN")
                recvGameState(simbolo)
                printBoard()

            elif message == "TIE":
                print("TIE")
                recvGameState(simbolo)
                printBoard()

            elif message == "VAL":
                print("VAL")
                recvGameState(simbolo)
                printBoard()
            
            if (message == "WIN" or message == "TIE") and endGameDecide():
                break
                
        elif message == "WAIT":
            message = client.recv(3).decode('ascii')

            if message == "DEF":
                print("DEF")
                recvGameState(1-simbolo)
                printBoard()

            elif message == "TIE":
                print("TIE")
                recvGameState(1-simbolo)
                printBoard()

            elif message == "VAL":
                print("VAL")
                recvGameState(1-simbolo)
                printBoard()
            
            if (message == "DEF" or message == "TIE") and endGameDecide():
                break

def connectToServer(ip, port):
    try:
        client.connect((ip, port))
    except:
        print("Server is not running")
        return False
    return True
    
def joinGame():
    if connectToServer('127.0.0.1', 55549) == False:
        return 'Server is not running'

    client.send("JOIN".encode('ascii'))
    print("JOIN")

    while True:
        message = client.recv(4).decode('ascii')
        print("MENSAGEM: " + message)
        if message != "IDRQ": break
        ID = input("Input ID: ")
        client.send(ID.encode('ascii'))

    nickname = input("Input NICK: ")
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    jogar()

def createGame():
    if connectToServer('127.0.0.1', 55549) == False:
        return 'Server is not running'
        
    client.send("CREATE".encode('ascii'))
    print("CREATE")

    message = client.recv(8).decode('ascii')
    ID = message
    print("MENSAGEM: " + ID)

    nickname = input("Input NICK: ")
    message = client.recv(4).decode('ascii')
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    print("WAINTING FOR PLAYER")
    message = client.recv(5).decode('ascii')
    print("MENSAGEM: " + message)
    if message == 'START': jogar()

def decide():
    escolha = input("Criar(1) ou Entrar(2) : "); print()

    if escolha == "1":
        createGame()    
    elif escolha == "2":
        joinGame()

decide()
