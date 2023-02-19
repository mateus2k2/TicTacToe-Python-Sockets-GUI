import socket
import threading

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

ID = ""
nickname = ""
board = [[]]

def resetGame():
    pass

def jogar():
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

    ID = "12345678"
    nickname = "jogador1"

    message = client.recv(1024).decode('ascii')
    while message == "IDREQUEST":
        message = client.recv(1024).decode('ascii')
        client.send(ID.encode('ascii'))

    # message = client.recv(1024).decode('ascii')
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    jogar()

def createGame():
    client.send("CREATE".encode('ascii'))

    ID = "0"
    nickname = "jogador1"

    message = client.recv(1024).decode('ascii')
    ID = message[3:]
    print(ID)

    message = client.recv(1024).decode('ascii')
    if message == 'NICK':
        client.send(nickname.encode('ascii'))

    message = client.recv(1024).decode('ascii')
    if message == 'START': jogar()


# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()