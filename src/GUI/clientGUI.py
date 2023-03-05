from tkinter import *
from tkinter import messagebox
import customtkinter
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
corSimbulos = ["#EE4035", "#0392CF"]    # X = vermelho, O = azul

host = '127.0.0.1'
port = 55553

class ClientGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Jogo da Velha")
        self.geometry("900x600")
        self.resizable(False, False)
        pygame.mixer.init()
        self.play_music()
        self.back_image = ImageTk.PhotoImage(Image.open("Images/back.png").resize((25, 25)))
        self.createMenuFrame()

    def createCanvas(self, master):
        canvas = customtkinter.CTkCanvas(master, width=900, height=600)
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
        self.settingsPageFrame = customtkinter.CTkFrame(self)
        self.settingsPageFrame.pack()
        self.settingsPageFrame.pack_propagate(False)
        self.settingsPageFrame.configure(width=900, height=600)
        self.settingsCanvas = self.createCanvas(self.settingsPageFrame)
        self.settingsCanvas.configure(bg="#1e1e1e")
        #self.settingsCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.settingsCanvas.create_text(450, 100, text="Configurações", font=("Impact", 80), fill = "white")
        self.settingsButtons()

    def set_volume(self, val):
        volume = int(val) / 100.0
        self.music.set_volume(volume)

    def set_theme(self, event):
        if self.tema.get() == "System":
            customtkinter.set_appearance_mode("System")
        elif self.tema.get() == "Light":
            customtkinter.set_appearance_mode("Light")
        elif self.tema.get() == "Dark":
            customtkinter.set_appearance_mode("Dark")

    def set_color(self, event):
        if self.cor.get() == "Azul-Escuro":
            customtkinter.set_default_color_theme("dark-blue")
        elif self.cor.get() == "Azul":
            customtkinter.set_default_color_theme("blue")
        elif self.cor.get() == "Verde":
            customtkinter.set_default_color_theme("green")

    def settingsButtons(self):
        self.settingsCanvas.create_text(450, 200, text="Volume", font=("Impact", 30), fill = "white")
        self.volume = customtkinter.CTkSlider(self.settingsCanvas, from_=0, to=100, command= lambda event: self.set_volume(self.volume.get()))
        self.settingsCanvas.create_window(450, 250, window=self.volume)
        self.settingsCanvas.create_text(450, 300, text="Tema", font=("Impact", 30), fill = "white")
        self.tema = customtkinter.CTkComboBox(self.settingsCanvas, values=["System", "Light", "Dark"], command= lambda event: self.set_theme(self.tema.get()))
        self.settingsCanvas.create_window(450, 350, window=self.tema)
        self.settingsCanvas.create_text(450, 400, text="Cor", font=("Impact", 30), fill = "white")
        self.cor = customtkinter.CTkComboBox(self.settingsCanvas, values=["Azul-Escuro", "Azul", "Verde"], command= lambda event: self.set_color(self.cor.get()))
        self.settingsCanvas.create_window(450, 450, window=self.cor)
        self.backButton = customtkinter.CTkButton(self.settingsCanvas, text="Voltar", font=("Impact", 30),image=self.back_image,compound= "left", command=lambda: self.backToMenu(self.settingsPageFrame))
        self.settingsCanvas.create_window(815, 570, window=self.backButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createMenuFrame(self):
        self.menuFrame = customtkinter.CTkFrame(self)
        self.menuFrame.pack()
        self.menuFrame.pack_propagate(False)
        self.menuFrame.configure(width=900, height=600)
        self.menuCanvas = self.createCanvas(self.menuFrame)
        self.menuCanvas.configure(bg="#1e1e1e")
        #self.image = ImageTk.PhotoImage(Image.open("Images/board.jpg").resize((900, 600)))
        #self.menuCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.MenuButtons()

    def MenuButtons(self):
        self.menuCanvas.create_text(450, 100, text="Jogo da Velha", font=("Impact", 80), fill = "#dee4ed")
        self.createGameButton = customtkinter.CTkButton(self.menuCanvas, text="Criar Jogo", font=("Impact", 30), command=self.createGameFrame)
        self.menuCanvas.create_window(450, 300, window=self.createGameButton)
        self.joinGameButton = customtkinter.CTkButton(self.menuCanvas, text="Entrar em Jogo", font=("Impact", 30), command=self.joinGameFrame)
        self.menuCanvas.create_window(450, 400, window=self.joinGameButton)
        self.exitButton = customtkinter.CTkButton(self.menuCanvas, text="Sair", font=("Impact", 30), command=self.destroy)
        self.menuCanvas.create_window(450, 500, window=self.exitButton)
        self.settings_image = ImageTk.PhotoImage(Image.open("Images/settings.png").resize((25, 25)))
        self.settingsButton = customtkinter.CTkButton(self.menuCanvas, text="Configurações", font=("Impact", 30),image=self.settings_image, compound="left", command=self.settingsFrame)
        #self.settingsButton = customtkinter.CTkButton(self.menuCanvas, text="",image=self.settings_image, command=self.settingsFrame, width=25, height=25)
        self.menuCanvas.create_window(775, 570, window=self.settingsButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def createGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.createGamePageFrame = customtkinter.CTkFrame(self)
        self.createGamePageFrame.pack()
        self.createGamePageFrame.pack_propagate(False)
        self.createGamePageFrame.configure(width=900, height=600)
        self.createGameCanvas = self.createCanvas(self.createGamePageFrame)
        self.createGameCanvas.configure(bg="#1e1e1e")
        #self.createGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.createGameCanvas.create_text(450, 100, text="Criar Jogo", font=("Impact", 80), fill = "white")
        self.createGameButtons()

    def createGameButtons(self):
        self.createGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        # self.NickEntry = Entry(self.createGameCanvas, font=("Impact", 30), width=20, textvariable="Maximo 25 Caracteres e Nao Pode Ser Vazio")
        self.NickEntry = customtkinter.CTkEntry(self.createGameCanvas, font=("Impact", 30), width=400)

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
        self.createGameButton = customtkinter.CTkButton(self.createGameCanvas, text="Criar Jogo", font=("Impact", 30), command=OkCallback)
        
        self.createGameCanvas.create_window(450, 400, window=self.createGameButton)
        self.backButton = customtkinter.CTkButton(self.createGameCanvas, text="Voltar", font=("Impact", 30), image=self.back_image, compound="left", command=lambda: self.backToMenu(self.createGamePageFrame))
        
        self.createGameCanvas.create_window(450, 500, window=self.backButton)

    def waitingRoomGUI(self, ID):
        self.clickSound()

        self.createGamePageFrame.destroy()

        self.waitingRoomPageFrame = customtkinter.CTkFrame(self)
        self.waitingRoomPageFrame.pack()
        self.waitingRoomPageFrame.pack_propagate(False)
        self.waitingRoomPageFrame.configure(width=900, height=600)

        self.waitingRoomCanvas = self.createCanvas(self.waitingRoomPageFrame)
        self.waitingRoomCanvas.configure(bg="#1e1e1e")
        #self.waitingRoomCanvas.create_image(0, 0, image=self.image, anchor=NW)
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
        self.joinGamePageFrame = customtkinter.CTkFrame(self)
        self.joinGamePageFrame.pack()
        self.joinGamePageFrame.pack_propagate(False)
        self.joinGamePageFrame.configure(width=900, height=600)
        self.joinGameCanvas = self.createCanvas(self.joinGamePageFrame)
        self.joinGameCanvas.configure(bg="#1e1e1e")
        #self.joinGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGameCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        self.joinGameButtons()

    def joinGameButtons(self):
        self.joinGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = "white")
        # self.NickEntry = Entry(self.joinGameCanvas, font=("Impact", 30), width=20, textvariable="Maximo 25 Caracteres e Nao Pode Ser Vazio")
        self.NickEntry = customtkinter.CTkEntry(self.joinGameCanvas, font=("Impact", 30), width=400)
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

        self.joinGameButton = customtkinter.CTkButton(self.joinGameCanvas, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.joinGameCanvas.create_window(450, 400, window=self.joinGameButton)
        self.backButton = customtkinter.CTkButton(self.joinGameCanvas, text="Voltar", font=("Impact", 30), image=self.back_image, compound="left" , command=lambda: self.backToMenu(self.joinGamePageFrame))
        self.joinGameCanvas.create_window(450, 500, window=self.backButton)

    def sendIDGUI(self): 
        self.clickSound()
        self.joinGamePageFrame.destroy()
        
        self.SendIDPageFrame = customtkinter.CTkButton(self)
        self.SendIDPageFrame.pack()
        self.SendIDPageFrame.pack_propagate(False)
        self.SendIDPageFrame.configure(width=900, height=600)
        self.SendIDCanvas = self.createCanvas(self.SendIDPageFrame)
        self.SendIDCanvas.configure(bg="#1e1e1e")
        #self.SendIDCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.SendIDCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = "white")
        
        self.SendIDCanvas.create_text(450, 200, text="Escolha ID:", font=("Impact", 30), fill = "white")
        self.IDEntry = customtkinter.CTkEntry(self.SendIDCanvas, font=("Impact", 30), width=400)
        self.SendIDCanvas.create_window(450, 250, window=self.IDEntry)
        
        def OkCallback():
            ID = self.IDEntry.get() # Get the value of the entry field

            if((not all(digito.isdigit() for digito in ID) and len(ID) != 8) or ID == ""):
                messagebox.showinfo("Error", "ID invalido")
                return
            
            if sendID(ID) == False:
                messagebox.showinfo("Error", "Room is not Available")
                return

            print("Jogar")
            self.play(self.joinGamePageFrame)
            

        self.SendIDButton = customtkinter.CTkButton(self.SendIDCanvas, text="Entrar", font=("Impact", 30), command = OkCallback)
        self.SendIDCanvas.create_window(450, 400, window=self.SendIDButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def resetGameGUI(self):
        for button in self.buttons:
            button.config(text= '', state=DISABLED)

        resetGame()

    def createPlayFrame(self, frame):
        frame.destroy()
        # ---------------------------------------------------------------------------------------------------

        self.playPageFrame = customtkinter.CTkFrame(self)
        self.playPageFrame.pack(fill=BOTH, expand=True)
        self.playPageFrame.pack_propagate(False)
        self.playPageFrame.configure(width=900, height=600)

        self.playCanvas = self.createCanvas(self.playPageFrame)
        self.playCanvas.pack(fill=BOTH, expand=True)
        self.playCanvas.pack_propagate(False)
        #self.playCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.playCanvas.configure(bg="#1e1e1e")
        
        self.playCanvas.create_text(450, 100, text="Jogando", font=("Impact", 80), fill = "white")
        
        self.textoJogarEsperar = self.playCanvas.create_text(450, 180, text="Jogando", font=("Impact", 20), fill="white")
        self.playCanvas.lift(self.textoJogarEsperar)
        
        self.textoPlacarMeu = self.playCanvas.create_text(225, 300, text="", font=("Impact", 20), fill="white")
        self.playCanvas.lift(self.textoPlacarMeu)
        
        self.textoPlacarAponente = self.playCanvas.create_text(675, 300, text="", font=("Impact", 20), fill="white")
        self.playCanvas.lift(self.textoPlacarAponente)

        buttonFrame = Frame(self.playCanvas, width=30, height=15)
        # meio x = 900 (largura do Frame) - 270 (Largura de todos os botões) / 2 = 315
        # meio y = 600 (altura do Frame) - 270 (altura de todos os botões) / 2 = 165
        buttonFrame.place(x=315, y=210) 

        self.img = ImageTk.PhotoImage(Image.open("Images/settings.png").resize((1, 1)))
        
        self.buttons = []
        for i in range(9):
            # mudar posicionamento dos botões para tem um espaço entre eles e colocar as linhas entre eles
            button = Button(buttonFrame, width=85, height=85, command=lambda i=i: self.turnPlay(i), state=DISABLED, font="cmr 80 bold", image=self.img, compound="left", bg="#1e1e1e", activebackground = "#1e1e1e", borderwidth=2)
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
        
        self.playPageFrame.place(x=0, y=0)

        self.backButton = Button(self.playCanvas, text="Sair", font=("Impact", 30), command = self.quit)
        self.playCanvas.create_window(450, 550, window=self.backButton)

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
        
        self.countDerrotas = 0
        self.countVitorias = 0
        self.countEmpates = 0

        self.playing = True
        self.buttonPressed = BooleanVar(value=False)

        # ---------------------------------------------------------------------------------------------------
        try:
            while self.playing:
                self.turn = getTurn()
                printBoard(); print()

                self.playCanvas.itemconfig(self.textoJogarEsperar, text=self.turn)
                self.playCanvas.itemconfig(self.textoPlacarMeu, text = self.nick + " = " + str(self.countVitorias))
                self.playCanvas.itemconfig(self.textoPlacarAponente, text = str(self.countDerrotas) + " = " + self.nickOponente)

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
                # self.buttons[position].config(text=simbolos[1 - self.simboloInt])
                self.buttons[position].config(text=simbolos[1 - self.simboloInt], state=DISABLED, disabledforeground = corSimbulos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Voce Perdeu")
                self.countDerrotas += 1

            elif message == "TIE":
                print("TIE")
                printBoard()
                position = recvGameState(1-self.simboloInt)
                # self.buttons[position].config(text=simbolos[1 - self.simboloInt])
                self.buttons[position].config(text=simbolos[1 - self.simboloInt], state=DISABLED, disabledforeground = corSimbulos[1 - self.simboloInt])
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")
                self.countEmpates += 1

            elif message == "VAL":
                print("VAL")
                printBoard()
                position = recvGameState(1-self.simboloInt)
                # self.buttons[position].config(text=simbolos[1 - self.simboloInt])
                self.buttons[position].config(text=simbolos[1 - self.simboloInt], state=DISABLED, disabledforeground = corSimbulos[1 - self.simboloInt])
            
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
        
        self.buttons[i].config(text=simbolos[self.simboloInt], state=DISABLED, disabledforeground = corSimbulos[self.simboloInt])
        # self.buttons[i].config(text=simbolos[self.simboloInt], state=DISABLED)
        
        try:
            message = sendMove(movimento)

            if message == "WIN":
                print("WIN")
                printBoard()
                recvGameState(self.simboloInt)
                messagebox.showinfo("Fim do Jogo", "Voce Ganhou")
                self.countVitorias += 1

            elif message == "TIE":
                print("TIE")
                printBoard()
                recvGameState(self.simboloInt)
                messagebox.showinfo("Fim do Jogo", "Jogo Empatado")
                self.countEmpates += 1

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

