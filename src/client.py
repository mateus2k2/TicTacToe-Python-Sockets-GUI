import socket
import threading

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55546))

ID = ""
nickname = ""
board = [['', '', ''],
         ['', '', ''],
         ['', '', ''],]

def resetGame():
    pass

def jogar():
    print("JOGANDO")
    movimento = "11"
    while True:
        message = client.recv(1024).decode('ascii')
        
        if message == 'TURN':
            client.send(movimento.encode('ascii'))
            message = client.recv(1024).decode('ascii')

            while message == "INVALID":
                client.send(movimento.encode('ascii'))
                message = client.recv(1024).decode('ascii')

            message = client.recv(1024).decode('ascii')
            if message == "WIN":
                print("You WIN")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            elif message == "TIE":
                print("Deu Empate")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            elif message == "VALID":
                print("Movimento Valido")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            
            if message == "LOOSE" or message == "TIE":
                client.send("CONTINUAR".encode('ascii'))
                resetGame()

        elif message == "WAIT":
            message = client.recv(1024).decode('ascii')
            if message == "LOOSE":
                print("You Loose")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            elif message == "TIE":
                print("Deu Empate")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            elif message == "VALID":
                print("Movimento Valido")
                message = client.recv(1024).decode('ascii')
                print("Movimento: " + message)
            
            if message == "LOOSE" or message == "TIE":
                client.send("CONTINUAR".encode('ascii'))
                resetGame()

def joinGame():
    client.send("JOIN".encode('ascii'))

    ID = "84947135"
    nickname = "jogador1"

    while True:
        message = client.recv(9).decode('ascii')
        print("MENSAGEM RECEBIDO JOIN 1: " + message)
        if message != "IDREQUEST": break
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

    message = client.recv(11).decode('ascii')
    ID = message[3:]
    print("MENSAGEM RECEBIDO CREATE 1: " + message + " Apenas ID: -" + ID + "-")

    message = client.recv(4).decode('ascii')
    print("MENSAGEM RECEBIDO CREATE 2: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    message = client.recv(1024).decode('ascii')
    print("MENSAGEM RECEBIDO CREATE 3: " + message)
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