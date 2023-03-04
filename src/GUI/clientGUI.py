from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame

import time
from queue import Queue
import threading

import sys
import os

client_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(client_dir)
from client import *

simbolos = ['X', 'O']

host = '127.0.0.1'
port = 55553

class ClientGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Velha")
        self.geometry("900x600")
        self.resizable(False, False)
        pygame.mixer.init()
        self.play_music()
        self.createMenuFrame()

    def createCanvas(self, master):
        canvas = Canvas(master, width=900, height=600)
        canvas.pack()
        return canvas

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def play_music(self):
        self.music = pygame.mixer.Sound("Sounds/Music.wav")
        self.music.set_volume(0)
        self.music.play(-1)

    def clickSound(self):
        click = pygame.mixer.Sound("Sounds/click.wav")
        click.play()

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def loadGifFrames(self):
        try:
            while True:
                self.loadingFrames.append(ImageTk.PhotoImage(self.loading.copy()))
                self.loading.seek(len(self.loadingFrames))
        except EOFError:
            pass

    def playGif(self, canvas, frame_index=0):
        canvas.create_image(800, 500, anchor='nw', image=self.loadingFrames[frame_index])

        nextFameIndex = (frame_index + 1) % len(self.loadingFrames)

        if not (self.eventThread.is_set()):
            canvas.after(3, self.playGif, canvas, nextFameIndex)

#------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def backToMenu(self, page):
        self.clickSound()
        page.destroy()
        self.createMenuFrame()

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def settingsFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.settingsPageFrame = Frame(self)
        self.settingsPageFrame.pack()
        self.settingsPageFrame.pack_propagate(False)
        self.settingsPageFrame.configure(width=900, height=600)
        self.settingsCanvas = self.createCanvas(self.settingsPageFrame)
        self.settingsCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.settingsCanvas.create_text(450, 100, text="Configurações", font=("Impact", 80), fill = "white")
        self.settingsButtons()

    def settingsButtons(self):
        self.settingsCanvas.create_text(450, 200, text="Configurações", font=("Impact", 30), fill = "white")
        self.volume = Scale(self.settingsCanvas, from_=0, to=100, orient=HORIZONTAL, length=300, font=("Impact", 30), command=lambda x: self.music.set_volume(int(x)/100))
        self.settingsCanvas.create_window(450, 300, window=self.volume)
        self.backButton = Button(self.settingsCanvas, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.settingsPageFrame))
        self.settingsCanvas.create_window(450, 500, window=self.backButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createMenuFrame(self):
        self.menuFrame = Frame(self)
        self.menuFrame.pack()
        self.menuFrame.pack_propagate(False)
        self.menuFrame.configure(width=900, height=600)
        self.menuCanvas = self.createCanvas(self.menuFrame)
        self.image = ImageTk.PhotoImage(Image.open("Images/board.jpg").resize((900, 600)))
        self.menuCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.MenuButtons()

    def MenuButtons(self):
        self.menuCanvas.create_text(450, 100, text="Jogo da Velha", font=("Impact", 80), fill = "white")
        self.createGameButton = Button(self.menuCanvas, text="Criar Jogo", font=("Impact", 30), command=self.createGameFrame)
        self.menuCanvas.create_window(450, 300, window=self.createGameButton)
        self.joinGameButton = Button(self.menuCanvas, text="Entrar em Jogo", font=("Impact", 30), command=self.joinGameFrame)
        self.menuCanvas.create_window(450, 400, window=self.joinGameButton)
        self.exitButton = Button(self.menuCanvas, text="Sair", font=("Impact", 30), command=self.destroy)
        self.menuCanvas.create_window(450, 500, window=self.exitButton)
        self.settingsButton = Button(self.menuCanvas, text="Configurações", font=("Impact", 30), command=self.settingsFrame)
        self.menuCanvas.create_window(775, 570, window=self.settingsButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.createGamePageFrame = Frame(self)
        self.createGamePageFrame.pack()
        self.createGamePageFrame.pack_propagate(False)
        self.createGamePageFrame.configure(width=900, height=600)
        self.createGameCanvas = self.createCanvas(self.createGamePageFrame)
        self.createGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.createGameCanvas.create_text(450, 100, text="Criar Jogo", font=("Impact", 80), fill = "white")
        self.createGameButtons()

    def createGameButtons(self):
        self.createGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        self.NickEntry = Entry(self.createGameCanvas, font=("Impact", 30), width=20, textvariable="Maximo 25 Caracteres e Nao Pode Ser Vazio")

        def OkCallback():
            self.nick = self.NickEntry.get() 
            
            if(len(self.nick) > 25 or self.nick == ""):
                messagebox.showinfo("Error", "nick invalido")
                return
            
            if connectToServer(host, port) == False:
                messagebox.showinfo("Error", "Server is not Running")
                return 

            IDVar = createGame(self.nick.ljust(25, "-")) 
            self.waitingRoomGUI(IDVar)

        self.createGameCanvas.create_window(450, 250, window=self.NickEntry)
        self.createGameButton = Button(self.createGameCanvas, text="Criar Jogo", font=("Impact", 30), command=OkCallback)
        
        self.createGameCanvas.create_window(450, 400, window=self.createGameButton)
        self.backButton = Button(self.createGameCanvas, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.createGamePageFrame))
        
        self.createGameCanvas.create_window(450, 500, window=self.backButton)

    def waitingRoomGUI(self, ID):
        self.clickSound()

        self.createGamePageFrame.destroy()

        self.waitingRoomPageFrame = Frame(self)
        self.waitingRoomPageFrame.pack()
        self.waitingRoomPageFrame.pack_propagate(False)
        self.waitingRoomPageFrame.configure(width=900, height=600)

        self.waitingRoomCanvas = self.createCanvas(self.waitingRoomPageFrame)
        self.waitingRoomCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.waitingRoomCanvas.create_text(450, 100, text="Sala de Esperda: ", font=("Impact", 80), fill = "white")
        self.waitingRoomCanvas.create_text(450, 350, text= "ID: " + str(ID), font=("Impact", 40), fill = "white")
        self.waitingRoomCanvas.create_text(450, 450, text= "Esperando Outro Jogador", font=("Impact", 40), fill = "white")

        self.loading = Image.open("images/loading.gif")
        self.loadingFrames = []
        self.loadGifFrames()

        self.eventThread = threading.Event()
        waitingRoomThread = threading.Thread(target=waitingRoom, args=(self.eventThread,))    
        waitingRoomThread.start()
        
        while not self.eventThread.is_set():
            self.playGif(self.waitingRoomCanvas)
            self.update()


        print("Jogar")
        self.play(self.waitingRoomPageFrame)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def joinGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.joinGamePageFrame = Frame(self)
        self.joinGamePageFrame.pack()
        self.joinGamePageFrame.pack_propagate(False)
        self.joinGamePageFrame.configure(width=900, height=600)
        self.joinGameCanvas = self.createCanvas(self.joinGamePageFrame)
        self.joinGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGameCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        self.joinGameButtons()

    def joinGameButtons(self):
        self.joinGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        self.NickEntry = Entry(self.joinGameCanvas, font=("Impact", 30), width=20, textvariable="Maximo 25 Caracteres e Nao Pode Ser Vazio")
        self.joinGameCanvas.create_window(450, 250, window=self.NickEntry)

        def OkCallback():
            self.nick = self.NickEntry.get() 
            
            if(len(self.nick) > 25 or self.nick == ""):
                messagebox.showinfo("Error", "nick invalido")
                return
            
            if connectToServer(host, port) == False:
                messagebox.showinfo("Error", "Server is not Running")
                return 

            joinGame(self.nick.ljust(25, "-"))
            self.sendIDGUI()

        self.joinGameButton = Button(self.joinGameCanvas, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.joinGameCanvas.create_window(450, 400, window=self.joinGameButton)
        self.backButton = Button(self.joinGameCanvas, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.joinGamePageFrame))
        self.joinGameCanvas.create_window(450, 500, window=self.backButton)

    def sendIDGUI(self): 
        self.clickSound()
        self.joinGamePageFrame.destroy()
        
        self.SendIDPageFrame = Frame(self)
        self.SendIDPageFrame.pack()
        self.SendIDPageFrame.pack_propagate(False)
        self.SendIDPageFrame.configure(width=900, height=600)
        self.SendIDCanvas = self.createCanvas(self.SendIDPageFrame)
        self.SendIDCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.SendIDCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        
        self.SendIDCanvas.create_text(450, 200, text="Escolha ID:", font=("Impact", 30), fill = "white")
        self.IDEntry = Entry(self.SendIDCanvas, font=("Impact", 30), width=20)
        self.SendIDCanvas.create_window(450, 250, window=self.IDEntry)
        
        def OkCallback():
            ID = self.IDEntry.get() # Get the value of the entry field

            if(not all(digito.isdigit() for digito in ID) and len(ID) != 8):
                messagebox.showinfo("Error", "ID invalido")
                return
            
            if sendID(ID) == False:
                messagebox.showinfo("Error", "Room is not Available")
                return

            print("Jogar")
            self.play(self.joinGamePageFrame)
            

        self.SendIDButton = Button(self.SendIDCanvas, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.SendIDCanvas.create_window(450, 400, window=self.SendIDButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def resetGameGUI(self):
        for button in self.buttons:
            button.config(text= '', state=DISABLED)

        resetGame()

    def createPlayFrame(self, frame):
        frame.destroy()
        # ---------------------------------------------------------------------------------------------------

        self.playPageFrame = Frame(self)
        self.playPageFrame.pack(fill=BOTH, expand=True)
        self.playPageFrame.pack_propagate(False)
        self.playPageFrame.configure(width=900, height=900)

        self.playCanvas = self.createCanvas(self.playPageFrame)
        self.playCanvas.pack(fill=BOTH, expand=True)
        self.playCanvas.pack_propagate(False)
        self.playCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.text_item = self.playCanvas.create_text(150, 150, text="Jogando", font=("Impact", 20), fill="white")
        self.playCanvas.lift(self.text_item) # bring the text item to the front

        # Create a frame inside the playCanvas canvas to hold the buttons
        buttonFrame = Frame(self.playCanvas, width=30, height=15)
        buttonFrame.pack(side=TOP, pady=10)

        self.buttons = []
        for i in range(9):
            button = Button(buttonFrame, width=10, height=5, command=lambda i=i: self.turnPlay(i), state=DISABLED)
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)


        self.playPageFrame.place(x=0, y=0)

        self.backButton = Button(self.playCanvas, text="Sair", font=("Impact", 30), command = self.quit)
        self.playCanvas.create_window(450, 500, window=self.backButton)

    def quit(self):
        # try:
        #     print("Quit Function")
        #     endGame()
        #     self.destroy()
        #     sys.exit()
        # except Exception as e:
        #     print("Error in quit function:", e)

        print("Quit Function")
        endGame()
        self.destroy()
        sys.exit()

    def play(self, frame):
        self.createPlayFrame(frame)

        # ---------------------------------------------------------------------------------------------------
        
        self.simboloInt = getSimbolo()
        self.nickOponente = getNickOponente().replace('-', '')
        print("nickOponente: " + self.nickOponente)

        self.playing = True
        self.buttonPressed = BooleanVar(value=False)

        # ---------------------------------------------------------------------------------------------------
        try:
            while self.playing:
                self.turn = getTurn()
                printBoard(); print()

                self.playCanvas.itemconfig(self.text_item, text=self.turn)

                time.sleep(2)

                print("TURNO: " + self.turn)

                if self.turn == 'PLAY': 
                    board = getBoard()
                    for i, button in enumerate(self.buttons):
                        if board[i//3][i%3] == '':
                            button.config(state=NORMAL)

                    self.wait_variable(self.buttonPressed)

                elif self.turn == 'WAIT':
                    self.turnWait()

                else:
                    raise Exception

        except Exception:
            self.playing = False
            self.quit()

    def endGameGUI(self):
        response = messagebox.askyesno("Fim do jogo", "Reiniciar o jogo?")

        event = threading.Event()
        fileResultado = Queue()
        endGameDecideThread = threading.Thread(target=endGameDecide, args=(response, event, fileResultado))
        endGameDecideThread.start()

        while not event.wait(1):
            self.update()

        self.playing = not fileResultado.get()

        if(self.playing == True):
            print("Reset GUI")
            self.resetGameGUI()
        else:
            print("Fim Game GUI")
            endGame()
            self.quit()

    def turnWait(self):
        try:
            # self.loading = Image.open("images/loading.gif")
            # self.loadingFrames = []
            # self.loadGifFrames()
            
            for i, button in enumerate(self.buttons):
                button.config(state=DISABLED)

            fileResultado = Queue()
            event = threading.Event()
            waitingRoomThread = threading.Thread(target=waitResponse, args=(event, fileResultado,))    
            waitingRoomThread.start()
            
            while not event.wait(1):
            # while not event.is_set():
                # print("GIF")
                # self.playGif(self.playCanvas)
                self.update()

            message = fileResultado.get()

            if message == "DEF":
                print("DEF")
                printBoard()
                position = recvGameState(1-self.simboloInt)
                self.buttons[position].config(text=simbolos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Voce Perdeu")

            elif message == "TIE":
                print("TIE")
                printBoard()
                position = recvGameState(1-self.simboloInt)
                self.buttons[position].config(text=simbolos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")

            elif message == "VAL":
                print("VAL")
                printBoard()
                position = recvGameState(1-self.simboloInt)
                self.buttons[position].config(text=simbolos[1 - self.simboloInt])
            
            elif message == "INV":
                print("INV")
                self.quit()
            
            if (message == "DEF" or message == "TIE"):
                self.endGameGUI()

        except:
            print("Trun Wait Error")
            self.playing = False
            
    def turnPlay(self, i):
        
        if i == 0: movimento = "11"
        if i == 1: movimento = "12"
        if i == 2: movimento = "13"
        if i == 3: movimento = "21"
        if i == 4: movimento = "22"
        if i == 5: movimento = "23"
        if i == 6: movimento = "31"
        if i == 7: movimento = "32"
        if i == 8: movimento = "33"
        
        self.buttons[i].config(text=simbolos[self.simboloInt], state=DISABLED)
        
        try:
            message = sendMove(movimento)

            if message == "WIN":
                print("WIN")
                printBoard()
                recvGameState(self.simboloInt)
                messagebox.showinfo("Fim do Jogo", "Voce Ganhou")

            elif message == "TIE":
                print("TIE")
                printBoard()
                recvGameState(self.simboloInt)
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")

            elif message == "VAL":
                print("VAL")
                printBoard()
                recvGameState(self.simboloInt)
            
            elif message == "INV":
                print("INV")
                self.quit()

            if (message == "WIN" or message == "TIE"):
                self.endGameGUI()

            self.buttonPressed.set(True)

        except:
            self.quit()
        

if __name__ == "__main__":
    client = ClientGUI()
    client.mainloop()
    sys.exit()

