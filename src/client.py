import socket
import threading

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55546))

simbolo = -1
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
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))

                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[simbolo]
                printBoard()

            elif message == "TIE":
                print("Deu Empate")
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))

                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[simbolo]
                printBoard()

            elif message == "VAL":
                print("Movimento Valido")
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))

                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[simbolo]
                printBoard()
            
            if message == "WIN" or message == "TIE":
                continuar = input("Escolha CNT ou END: ")
                client.send(continuar.encode('ascii'))
                continuar = client.recv(3).decode('ascii')

                if continuar == "CNT":
                    print("Resetando o Jogo")
                    resetGame()
                elif continuar == "END":
                    print("Encerando o Jogo")
                    endGame()
                    break

        elif message == "WAIT":
            message = client.recv(3).decode('ascii')

            if message == "DEF":
                print("You Loose")
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))
                
                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[1 - simbolo]
                printBoard()

            elif message == "TIE":
                print("Deu Empate")
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))

                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[1 - simbolo]
                printBoard()

            elif message == "VAL":
                print("Movimento Valido")
                movimento = int(client.recv(2).decode('ascii'))
                print("Movimento: " + str(movimento))

                linha = int(movimento // 10) - 1
                coluna = int(movimento % 10) - 1
                board[linha][coluna] = simbolos[1 - simbolo]
                printBoard()
            
            if message == "DEF" or message == "TIE":
                continuar = input("Escolha CNT ou END: ")
                client.send(continuar.encode('ascii'))
                continuar = client.recv(3).decode('ascii')

                if continuar == "CNT":
                    print("Resetando o Jogo")
                    resetGame()
                elif continuar == "END":
                    print("Encerando o Jogo")
                    endGame()
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

    # message = client.recv(4).decode('ascii')
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

    # message = client.recv(4).decode('ascii')
    # print("MENSAGEM RECEBIDO CREATE 3: " + message)
    # if message == 'SINB':
    #     client.send(str(sinbolo).encode('ascii'))

    message = client.recv(5).decode('ascii')
    print("MENSAGEM RECEBIDO CREATE 4: " + message)
    if message == 'START': jogar()

escolha = input("Entrar(0) ou Criar(1): ")

if escolha == "0":
    joinGame()
elif escolha == "1":
    createGame()

# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()