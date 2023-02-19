import socket
import threading

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55546))

simbolo = -1
ID = ""
nickname = ""

simbolos = ['X', 'O']
board = [['', '', ''],
         ['', '', ''],
         ['', '', ''],]

def resetGame():
    pass

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
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            elif message == "TIE":
                print("Deu Empate")
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            elif message == "VAL":
                print("Movimento Valido")
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            
            if message == "DEF" or message == "TIE":
                client.send("CONTINUAR".encode('ascii'))
                resetGame()

        elif message == "WAIT":
            message = client.recv(3).decode('ascii')

            if message == "DEF":
                print("You Loose")
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            elif message == "TIE":
                print("Deu Empate")
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            elif message == "VAL":
                print("Movimento Valido")
                message = client.recv(2).decode('ascii')
                print("Movimento: " + message)
            
            if message == "DEF" or message == "TIE":
                client.send("CONTINUAR".encode('ascii'))
                resetGame()

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