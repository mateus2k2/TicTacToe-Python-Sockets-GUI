import socket

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55547))

# simbolo = -1
ID = ""
nickname = ""
board = [['', 'O', 'X'],
         ['X', 'O', 'X'],
         ['O', 'X', 'O'],]

simbolos = ['X', 'O']

def printBoard():
    for row in board:
        for item in row:
            print(item, end=" ")
        print()

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

    print("Movimento: " + str(movimento))

def endGameDecide():
    continuar = input("Escolha CNT ou END: ")
    client.send(continuar.encode('ascii'))
    continuar = client.recv(3).decode('ascii')

    if continuar == "CNT":
        print("Resetando o Jogo")
        resetGame()
        return False
    elif continuar == "END":
        print("Encerando o Jogo")
        endGame()
        return True

def jogar():
    print("\nJOGANDO")
    movimento = ""

    simbolo = int(client.recv(1).decode('ascii'))
    print("SIMBOLO: " + simbolos[simbolo])

    while True:
        message = client.recv(4).decode('ascii')
        print("MENSAGEM TURNO: " + message)

        if message == 'PLAY':

            while True:
                movimento = input("Digite o Movimento: ")
                client.send(movimento.encode('ascii'))
                message = client.recv(3).decode('ascii'); print("MENSAGEM: " + message)
                if message != "INV": break

            # message = client.recv(5).decode('ascii')
            if message == "WIN":
                print("You WIN")
                recvGameState(simbolo)
                printBoard()

            elif message == "TIE":
                print("Deu Empate")
                recvGameState(simbolo)
                printBoard()

            elif message == "VAL":
                print("Movimento Valido")
                recvGameState(simbolo)
                printBoard()
            
            if (message == "WIN" or message == "TIE") and endGameDecide():
                break
                
        elif message == "WAIT":
            message = client.recv(3).decode('ascii')

            if message == "DEF":
                print("You Loose")
                recvGameState(simbolo)
                printBoard()

            elif message == "TIE":
                print("Deu Empate")
                recvGameState(simbolo)
                printBoard()

            elif message == "VAL":
                print("Movimento Valido")
                recvGameState(simbolo)
                printBoard()
            
            if (message == "DEF" or message == "TIE") and endGameDecide():
                break

def joinGame():
    client.send("JOIN".encode('ascii'))

    ID = "84947135"
    nickname = "jogador1"

    while True:
        message = client.recv(4).decode('ascii')
        print("MENSAGEM RECEBIDO JOIN 1: " + message)
        if message != "IDRQ": break
        ID = input("Digite o ID: ")
        client.send(ID.encode('ascii'))

    print("MENSAGEM RECEBIDO JOIN 2: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    jogar()

def createGame():
    client.send("CREATE".encode('ascii'))

    ID = "0"
    nickname = "jogador1"
    sinbolo = 0

    message = client.recv(8).decode('ascii')
    ID = message
    print("MENSAGEM RECEBIDO CREATE 1: " + message)

    message = client.recv(4).decode('ascii')
    print("MENSAGEM RECEBIDO CREATE 2: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    message = client.recv(5).decode('ascii')
    print("MENSAGEM RECEBIDO CREATE 4: " + message)
    if message == 'START': jogar()

escolha = input("Entrar(0) ou Criar(1): ")

if escolha == "0":
    joinGame()
elif escolha == "1":
    createGame()    