import socket
import json

# Connecting To Server
client = None

# inicializa o jogo
board = [['', '', ''],
         ['', '', ''],
         ['', '', ''],]

# vetor auxiliar para determinar o simbolo do jogador
simbolos = ['X', 'O']

#------------------------------------------------UTILITÁRIOS--------------------------------------------------------------------------------------

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

def resetBoad():
    board[0][0] = ''; board[0][1] = ''; board[0][2]  = '';
    board[1][0] = ''; board[1][1] = ''; board[1][2]  = '';
    board[2][0] = ''; board[2][1] = ''; board[2][2]  = '';

def endGame():
    board[0][0] = ''; board[0][1] = ''; board[0][2]  = '';
    board[1][0] = ''; board[1][1] = ''; board[1][2]  = '';
    board[2][0] = ''; board[2][1] = ''; board[2][2]  = '';
    client.close()

#------------------------------------------------JOGO EM SI--------------------------------------------------------------------------------------

def recvGameState(simbolo):
    #Recebe o movimento do oponente ou o proprio movimento
    movimento = int(client.recv(2).decode('ascii'))
    #Converte o movimento para a posição do tabuleiro (Ex 11 = Linha 0, Coluna 0)
    linha = int(movimento // 10) - 1
    coluna = int(movimento % 10) - 1
    #Preenche a posição do tabuleiro com o simbolo do jogador
    board[linha][coluna] = simbolos[simbolo]
    
    #Converte o movimento para posição correspondente em um vetor de 9 posições 
    #Vai ser usado no vetor de botoes da GUI
    movDict = {11: 0, 12: 1, 13: 2, 21: 3,  22: 4, 23: 5, 31: 6, 32: 7, 33: 8}
    returno = movDict.get(movimento, -1)

    print("MOVIMENTO: " + str(movimento))

    return returno

def endGameDecide(response, event, fileResultado):
    # Se response for True o jogo continua
    if response == True:
        continuar = 'CNT'
    # Se nao response for True o jogo acaba
    else:
        continuar = 'END'
    # Envia CNT ou END para o servidor
    client.send(continuar.encode('ascii'))
    
    # Se continuar não for END entao o jogador precisar esperar a  resposta do servidor para saber se outro jogador quer continuar 
    print("ESPERANDO RESPOSTA SERVER")
    continuar = client.recv(3).decode('ascii')

    # Se a resposta do servirdor for CNT então os dois jogadores querem continuar 
    if continuar == "CNT":
        print("RESET GAME")
        event.set()
        fileResultado.put(False)
        return False
    
    # Se continuar for END entao o jogador decidiu acabar o jogo então pode sair
    if continuar == "END":
        print("FIM JOGO")
        event.set()
        fileResultado.put(True)
        return True

def getNickOponente():
    nicknameOpodente = client.recv(25).decode('ascii')
    return nicknameOpodente
 
def getSimbolo():
    simbolo = int(client.recv(1).decode('ascii'))
    return simbolo

def getTurn():
    message = client.recv(4).decode('ascii')
    print("MENSAGEM: " + message)
    return message

def sendMove(movimentoGUI):
    # manda o movimento para o servidor
    client.send(movimentoGUI.encode('ascii'))
    # Recebe a resposta do servidor = WIN, TIE, VAL, INV 
    message = client.recv(3).decode('ascii'); print("MENSAGEM: " + message)
    return message

def waitResponse(event, fileResultado):
    try:
        # Função onde o jogador que não esta jogando fica esperando a resposta do servidor
        # Espera a mensagem do servidor = DEF, TIE, VAL, INV
        message = client.recv(3).decode('ascii')
        fileResultado.put(message)
        event.set()
        return message
    except:
        print("ERROR")

def getBoard():
    return board

#-----------------------------------------------CONECTAR NO SERVER---------------------------------------------------------------------------------------

def connectToServer(ip, port):
    global client
    
    # Tenta conectar no servidor
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # Recebe a resposta do servidor = OK, FULL
        resposta = client.recv(4).decode('ascii')
        if(resposta == "OK"):
            return True
        elif(resposta == "FULL"):
            print("Server is full")
            return False
    # Caso tenha error returna False
    except:
        print("Server is not running")
        return False

#-----------------------------------------------ENTRAR EM JOGO IA-----------------------------------------------------------------------------------------

def joinGameIA(GUINick, dificultade):
    client.send("JOINIA".encode('ascii')) # Manda join para o servidor
    print("JOINIA")

    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = NICK
    nickname = GUINick
    if message == 'NICK':
        client.send(nickname.encode('ascii')) # Manda o nickname para o servidor
        
    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = NICK
    nickname = GUINick
    if message == 'DIFC':
        client.send(dificultade.encode('ascii')) # Manda o nickname para o servidor

#------------------------------------------------ENTRAR EM JOGO--------------------------------------------------------------------------------------------

def joinGame(GUINick):
    client.send("JOIN".encode('ascii')) # Manda join para o servidor
    print("JOIN")

    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = NICK
    nickname = GUINick
    if message == 'NICK':
        client.send(nickname.encode('ascii')) # Manda o nickname para o servidor

def sendID(GUIID):
    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = IDRQ
    ID = GUIID
    client.send(ID.encode('ascii')) # Manda o ID para o servidor
    print("MENSAGEM: " + message)
    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = IDOK ou IDRQ
    if message != "IDRQ": return True
    return False

#------------------------------------------------CRIAR JOGO----------------------------------------------------------------------------------------

def createGame(GUINick):
    client.send("CREATE".encode('ascii')) # Manda create para o servidor
    print("CREATE")

    message = client.recv(8).decode('ascii') # Recebe a resposta do servidor = ID
    ID = message
    print("MENSAGEM: " + ID)

    nickname = GUINick
    message = client.recv(4).decode('ascii') # Recebe a resposta do servidor = nick
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii')) # Manda o nickname para o servidor

    return ID

def waitingRoom(event):
    print("WAINTING FOR PLAYER")
    # Quando outro jogador entrar na sala o servidor manda a mensagem START
    message = client.recv(5).decode('ascii') 
    print("MENSAGEM: " + message)
    if message == 'START': 
        event.set()
        return True
    return False

#-----------------------------------------------LOGIN REGISTER E RANK------------------------------------------------------------------------------------------

def sendLoginRegister(nickGUI, passwordGUI, option):
    client.send(option.encode('ascii')) # Manda LOGIN/REG para o servidor
    print(option)

    nickname = nickGUI
    message = client.recv(4).decode('ascii') 
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))
        
    password = passwordGUI
    message = client.recv(4).decode('ascii') 
    print("MENSAGEM: " + message)
    if message == 'PASS':
        client.send(password.encode('ascii'))

    message = client.recv(4).decode('ascii') 
    client.close()

    if(message == "LGOK" or message == "RGOK"):
        return True
    elif(message == "LGNO" or message == "RGNO"):
        return False

def sendLoginState(loggedIn):
    print("loggedIn " + str(loggedIn))
    if(loggedIn):
        client.send("LOGIN".encode('ascii'))
    else:
        client.send("LOGNO".encode('ascii'))

def getUserStats(nickGUI):
    client.send("URSST".encode('ascii')) 
    print("URSST: " + nickGUI)

    message = client.recv(4).decode('ascii') 
    nickname = nickGUI
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))
    
    print("Recebendo dados do servidor")
    user_data = client.recv(1024).decode()
    user_dict = json.loads(user_data)

    client.close()
    
    return user_dict

def getRankStats():
    client.send("RNKST".encode('ascii')) 

    print("Recebendo dados do servidor")
    table_json = ""
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        table_json += data
    table_data = json.loads(table_json)

    client.close()
    
    return table_data

def sendLogOut(nickGUI):
    client.send("LOGOT".encode('ascii')) # Manda LOGIN/REG para o servidor

    nickname = nickGUI
    message = client.recv(4).decode('ascii') 
    print("MENSAGEM: " + message)
    if message == 'NICK':
        client.send(nickname.encode('ascii'))
        
    client.close()