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

class ClientGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Velha")
        self.geometry("900x600")
        self.resizable(False, False)
        pygame.mixer.init()
        self.play_music()
        self.createMenuFrame()

    def createImages(self):
        self.image = ImageTk.PhotoImage(Image.open("Images/board.jpg").resize((900, 600)))

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
        # Display the current frame of the GIF image
        canvas.create_image(800, 500, anchor='nw', image=self.loadingFrames[frame_index])

        # Go to the next frame of the GIF image
        next_frame_index = (frame_index + 1) % len(self.loadingFrames)

        # Check if the thread is still running
        if not (self.eventThread.is_set()):
            # Schedule the next frame of the GIF image to be displayed
            canvas.after(3, self.playGif, canvas, next_frame_index)

#------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def backToMenu(self, page):
        self.clickSound()
        page.destroy()
        self.createMenuFrame()

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def settingsFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.settingsPage = Frame(self)
        self.settingsPage.pack()
        self.settingsPage.pack_propagate(False)
        self.settingsPage.configure(width=900, height=600)
        self.settings = self.createCanvas(self.settingsPage)
        self.settings.create_image(0, 0, image=self.image, anchor=NW)
        self.settings.create_text(450, 100, text="Configurações", font=("Impact", 80), fill = "white")
        self.settingsButtons()

    def settingsButtons(self):
        self.settings.create_text(450, 200, text="Configurações", font=("Impact", 30), fill = "white")
        self.volume = Scale(self.settings, from_=0, to=100, orient=HORIZONTAL, length=300, font=("Impact", 30), command=lambda x: self.music.set_volume(int(x)/100))
        self.settings.create_window(450, 300, window=self.volume)
        self.backButton = Button(self.settings, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.settingsPage))
        self.settings.create_window(450, 500, window=self.backButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createMenuFrame(self):
        self.menuFrame = Frame(self)
        self.menuFrame.pack()
        self.menuFrame.pack_propagate(False)
        self.menuFrame.configure(width=900, height=600)
        self.menu = self.createCanvas(self.menuFrame)
        self.createImages()
        self.menu.create_image(0, 0, image=self.image, anchor=NW)
        self.MenuButtons()

    def MenuButtons(self):
        self.menu.create_text(450, 100, text="Jogo da Velha", font=("Impact", 80), fill = "white")
        self.createGameButton = Button(self.menu, text="Criar Jogo", font=("Impact", 30), command=self.createGameFrame)
        self.menu.create_window(450, 300, window=self.createGameButton)
        self.joinGameButton = Button(self.menu, text="Entrar em Jogo", font=("Impact", 30), command=self.joinGameFrame)
        self.menu.create_window(450, 400, window=self.joinGameButton)
        self.exitButton = Button(self.menu, text="Sair", font=("Impact", 30), command=self.destroy)
        self.menu.create_window(450, 500, window=self.exitButton)
        self.settingsButton = Button(self.menu, text="Configurações", font=("Impact", 30), command=self.settingsFrame)
        self.menu.create_window(775, 570, window=self.settingsButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.createGamePage = Frame(self)
        self.createGamePage.pack()
        self.createGamePage.pack_propagate(False)
        self.createGamePage.configure(width=900, height=600)
        self.createGame = self.createCanvas(self.createGamePage)
        self.createGame.create_image(0, 0, image=self.image, anchor=NW)
        self.createGame.create_text(450, 100, text="Criar Jogo", font=("Impact", 80), fill = "white")
        self.createGameButtons()

    def createGameButtons(self):
        self.createGame.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        self.gameNameEntry = Entry(self.createGame, font=("Impact", 30), width=20)

        def OkCallback():
            nick = self.gameNameEntry.get() 
            IP = '127.0.0.1' # IPEntry.get()
            Port = 55599 # PortEntry.get()

            if connectToServer(IP, int(Port)) == False:
                messagebox.showinfo("Error", "Server is not Running")
                return 

            IDVar = createGame(nick) 
            self.waitingRoomGUI(IDVar)

        self.createGame.create_window(450, 250, window=self.gameNameEntry)
        self.createGameButton = Button(self.createGame, text="Criar Jogo", font=("Impact", 30), command=OkCallback)
        
        self.createGame.create_window(450, 400, window=self.createGameButton)
        self.backButton = Button(self.createGame, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.createGamePage))
        
        self.createGame.create_window(450, 500, window=self.backButton)

    def waitingRoomGUI(self, ID):
        self.clickSound()

        self.createGamePage.destroy()

        self.waitingRoomPage = Frame(self)
        self.waitingRoomPage.pack()
        self.waitingRoomPage.pack_propagate(False)
        self.waitingRoomPage.configure(width=900, height=600)

        self.waitingRoom = self.createCanvas(self.waitingRoomPage)
        self.waitingRoom.create_image(0, 0, image=self.image, anchor=NW)
        self.waitingRoom.create_text(450, 100, text="Waiting Room ID: ", font=("Impact", 80), fill = "white")
        self.waitingRoom.create_text(450, 250, text= str(ID), font=("Impact", 80), fill = "white")

        self.loading = Image.open("images/loading.gif")
        self.loadingFrames = []
        self.loadGifFrames()

        self.eventThread = threading.Event()
        waitingRoomThread = threading.Thread(target=waitingRoom, args=(self.eventThread,))    
        waitingRoomThread.start()
        
        while not self.eventThread.is_set():
            self.playGif(self.waitingRoom)
            self.update()


        print("Jogar")
        self.play(2)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def joinGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.joinGamePage = Frame(self)
        self.joinGamePage.pack()
        self.joinGamePage.pack_propagate(False)
        self.joinGamePage.configure(width=900, height=600)
        self.joinGame = self.createCanvas(self.joinGamePage)
        self.joinGame.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGame.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        self.joinGameButtons()

    def joinGameButtons(self):
        self.joinGame.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        self.gameNameEntry = Entry(self.joinGame, font=("Impact", 30), width=20)
        self.joinGame.create_window(450, 250, window=self.gameNameEntry)

        def OkCallback():
            nick = self.gameNameEntry.get() 
            IP = '127.0.0.1' # IPEntry.get()
            Port = 55599 # PortEntry.get()

            if connectToServer(IP, int(Port)) == False:
                messagebox.showinfo("Error", "Server is not Running")
                return 

            joinGame(nick)
            self.sendIDGUI()

        self.joinGameButton = Button(self.joinGame, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.joinGame.create_window(450, 400, window=self.joinGameButton)
        self.backButton = Button(self.joinGame, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.joinGamePage))
        self.joinGame.create_window(450, 500, window=self.backButton)

    def sendIDGUI(self): 
        self.clickSound()
        self.joinGamePage.destroy()
        
        self.SendIDPage = Frame(self)
        self.SendIDPage.pack()
        self.SendIDPage.pack_propagate(False)
        self.SendIDPage.configure(width=900, height=600)
        self.SendID = self.createCanvas(self.SendIDPage)
        self.SendID.create_image(0, 0, image=self.image, anchor=NW)
        self.SendID.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        
        self.SendID.create_text(450, 200, text="Escolha ID:", font=("Impact", 30), fill = "white")
        self.IDEntry = Entry(self.SendID, font=("Impact", 30), width=20)
        self.SendID.create_window(450, 250, window=self.IDEntry)
        
        def OkCallback():
            ID = self.IDEntry.get() # Get the value of the entry field

            if sendID(ID) == False:
                messagebox.showinfo("Error", "Room is not Available")
                return

            print("Jogar")
            self.play(1)

        self.SendIDButton = Button(self.SendID, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.SendID.create_window(450, 400, window=self.SendIDButton)
        self.backButton = Button(self.SendID, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.SendIDPage))
        self.SendID.create_window(450, 500, window=self.backButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def resetGameGUI(self):
        for button in self.buttons:
            button.config(text= '', state=DISABLED)

        self.buttonsDisable = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        resetGame()

    def createPlayFrame(self, flag):
        if flag == 1:
            self.SendIDPage.destroy()
        elif flag == 2:
            self.waitingRoomPage.destroy()

        # ---------------------------------------------------------------------------------------------------

        self.playPage = Frame(self)
        self.playPage.pack(fill=BOTH, expand=True)
        self.playPage.pack_propagate(False)
        self.playPage.configure(width=900, height=900)

        self.play = self.createCanvas(self.playPage)
        self.play.pack(fill=BOTH, expand=True)
        self.play.pack_propagate(False)
        self.play.create_image(0, 0, image=self.image, anchor=NW)
        self.text_item = self.play.create_text(150, 150, text="Jogando", font=("Impact", 20), fill="white")
        self.play.lift(self.text_item) # bring the text item to the front

        # Create a frame inside the play canvas to hold the buttons
        buttonFrame = Frame(self.play, width=30, height=15)
        buttonFrame.pack(side=TOP, pady=10)

        self.buttons = []
        self.buttonsDisable = [0, 1, 1, 1, 1, 1, 1, 1, 1]

        for i in range(9):
            button = Button(buttonFrame, width=10, height=5, command=lambda i=i: self.turnPlay(i), state=DISABLED)
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)


            #encerrar o jogo e mandar aviso pro outro cliente
        # Position the playPage frame anywhere on the screen
        self.playPage.place(x=0, y=0)

        self.backButton = Button(self.play, text="Sair", font=("Impact", 30), command = self.quit)
        self.play.create_window(450, 500, window=self.backButton)

    def quit(self):
        print("Quit Function")
        endGame()
        self.destroy()
        sys.exit()

    def play(self, flag):
        self.createPlayFrame(flag)

        # ---------------------------------------------------------------------------------------------------
        
        self.simboloInt = getSimbolo()

        self.playing = True
        self.button_pressed = BooleanVar(value=False)

        # ---------------------------------------------------------------------------------------------------
        try:
            while self.playing:
                self.turn = getTurn()
                printBoard(); print()

                self.play.itemconfig(self.text_item, text=self.turn)

                time.sleep(2)

                print("TURNO: " + self.turn)

                if self.turn == 'PLAY': 
                    var = 0
                    for button in self.buttons:
                        if(self.buttonsDisable[var] == 0):
                            button.config(state=NORMAL)
                        var += 1

                    self.wait_variable(self.button_pressed)

                elif self.turn == 'WAIT':
                    self.turnWait()

                else:
                    raise Exception

        except:
            self.quit()
            self.playing = False

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
            fileResultado = Queue()
            event = threading.Event()
            waitingRoomThread = threading.Thread(target=waitResponse, args=(event, fileResultado,))    
            waitingRoomThread.start()
            
            while not event.wait(1):
                self.update()

            message = fileResultado.get()

            if message == "DEF":
                print("DEF")
                var = recvGameState(1-self.simboloInt)
                self.buttonsDisable[var] = 1
                self.buttons[var].config(text=simbolos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Voce Perdeu")
                printBoard()

            elif message == "TIE":
                print("TIE")
                var = recvGameState(1-self.simboloInt)
                self.buttonsDisable[var] = 1
                self.buttons[var].config(text=simbolos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")
                printBoard()

            elif message == "VAL":
                print("VAL")
                var = recvGameState(1-self.simboloInt)
                self.buttonsDisable[var] = 1
                self.buttons[var].config(text=simbolos[1 - self.simboloInt])
                printBoard()
            
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
        self.buttonsDisable[i] = 1
        
        try:
            message = sendMove(movimento)

            if message == "WIN":
                print("WIN")
                recvGameState(self.simboloInt)
                printBoard()
                messagebox.showinfo("Fim do Jogo", "Voce Ganhou")

            elif message == "TIE":
                print("TIE")
                recvGameState(self.simboloInt)
                printBoard()
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")

            elif message == "VAL":
                print("VAL")
                recvGameState(self.simboloInt)
                printBoard()
            
            elif message == "INV":
                print("INV")
                self.quit()

            if (message == "WIN" or message == "TIE"):
                self.endGameGUI()

            self.button_pressed.set(True)

        except:
            self.quit()
        

if __name__ == "__main__":
    client = ClientGUI()
    client.mainloop()
    sys.exit()

