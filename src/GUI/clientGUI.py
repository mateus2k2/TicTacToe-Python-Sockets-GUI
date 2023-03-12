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
        self.text_color = "white"
        self.bg_color = "#1e1e1e"
        self.loggedIn = False
        self.usrName = ""
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

    # def loadGifFrames(self):
    #     try:
    #         while True:
    #             self.loadingFrames.append(ImageTk.PhotoImage(self.loading.copy()))
    #             self.loading.seek(len(self.loadingFrames))
    #     except EOFError:
    #         pass

    # def playGif(self, canvas, event, frame_index=0):
    #     self.loading_id = canvas.create_image(790, 490, anchor='nw', image=self.loadingFrames[frame_index])

    #     nextFameIndex = (frame_index + 1) % len(self.loadingFrames)

    #     if not (event.is_set()):
    #         canvas.after(3, self.playGif, canvas, event, nextFameIndex)
    #     else:
    #         canvas.delete(self.loading_id)

#-----------------------------------------------------------------------------------------------------------------------
            
    def backToMenu(self, page):
        self.clickSound()
        page.destroy()
        self.createMenuFrame()

#------------------------------------------------CONFIGURAÇÕES----------------------------------------------------------------------

    def settingsFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.settingsPageFrame = customtkinter.CTkFrame(self)
        self.settingsPageFrame.pack()
        self.settingsPageFrame.pack_propagate(False)
        self.settingsPageFrame.configure(width=900, height=600)
        self.settingsCanvas = self.createCanvas(self.settingsPageFrame)
        self.settingsCanvas.configure(bg=self.bg_color)
        #self.settingsCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.settingsCanvas.create_text(450, 100, text="Configurações", font=("Impact", 80), fill = self.text_color)
        self.settingsButtons()

    def set_volume(self, val):
        volume = int(val) / 100.0
        self.music.set_volume(volume)

    def set_theme(self, event):
        if self.tema.get() == "System":
            customtkinter.set_appearance_mode("System")
        elif self.tema.get() == "Light":
            self.bg_color = "#dee4ed"
            self.text_color = "#1e1e1e"
            customtkinter.set_appearance_mode("Light")
        elif self.tema.get() == "Dark":
            self.text_color = "#dee4ed"
            self.bg_color = "#1e1e1e"
            customtkinter.set_appearance_mode("Dark")

    def set_color(self, event):
        if self.cor.get() == "Azul-Escuro":
            customtkinter.set_default_color_theme("dark-blue")
        elif self.cor.get() == "Azul":
            customtkinter.set_default_color_theme("blue")
        elif self.cor.get() == "Verde":
            customtkinter.set_default_color_theme("green")

    def settingsButtons(self):
        self.settingsCanvas.create_text(450, 200, text="Volume", font=("Impact", 30), fill = self.text_color)
        self.volume = customtkinter.CTkSlider(self.settingsCanvas, from_=0, to=100 , command= lambda event: self.set_volume(self.volume.get()))
        self.settingsCanvas.create_window(450, 250, window=self.volume)
        self.settingsCanvas.create_text(450, 300, text="Tema", font=("Impact", 30), fill = self.text_color)
        self.tema = customtkinter.CTkComboBox(self.settingsCanvas, values=["", "System", "Light", "Dark"], command= lambda event: self.set_theme(self.tema.get()))
        self.settingsCanvas.create_window(450, 350, window=self.tema)
        self.settingsCanvas.create_text(450, 400, text="Cor", font=("Impact", 30), fill = self.text_color)
        self.cor = customtkinter.CTkComboBox(self.settingsCanvas, values=["", "Azul-Escuro", "Azul", "Verde"], command= lambda event: self.set_color(self.cor.get()))
        self.settingsCanvas.create_window(450, 450, window=self.cor)
        self.backButton = customtkinter.CTkButton(self.settingsCanvas, text="Voltar", text_color= self.text_color, font=("Impact", 30),image=self.back_image,compound= "left", command=lambda: self.backToMenu(self.settingsPageFrame))
        self.settingsCanvas.create_window(815, 570, window=self.backButton)
        
        self.settingsCanvas.create_text(700, 200, text="IP:", font=("Impact", 30), fill = self.text_color)
        self.IPEntry = customtkinter.CTkEntry(self.settingsCanvas, width=200, font=("Impact", 30), placeholder_text_color = "#c0c0c0")
        self.settingsCanvas.create_window(700, 250, window=self.IPEntry)
        self.settingsCanvas.create_text(700, 300, text="Porta:", font=("Impact", 30), fill = self.text_color)
        self.PortEntry = customtkinter.CTkEntry(self.settingsCanvas, width=200, font=("Impact", 30), placeholder_text_color = "#c0c0c0")
        self.settingsCanvas.create_window(700, 350, window=self.PortEntry)
        self.loginButton = customtkinter.CTkButton(self.settingsCanvas, text="Mudar", text_color= self.text_color, font=("Impact", 30), command=self.modifieIpPort)
        self.settingsCanvas.create_window(700, 450, window=self.loginButton)
        
        self.IPEntry.configure(placeholder_text = host)
        self.PortEntry.configure(placeholder_text = port)

    def modifieIpPort(self):
        global host, port
        
        self.clickSound()
        IPEntryValue = self.IPEntry.get()
        PortEntryValue = self.PortEntry.get()
        
        if(IPEntryValue == "" or PortEntryValue == "" or PortEntryValue.isnumeric() == False or IPEntryValue.replace('.', '').isnumeric() == False):
            messagebox.showinfo("Error", "Valores Imvalidos")
            return
        else:
            host = IPEntryValue
            port = int(PortEntryValue)
        
        self.IPEntry.configure(placeholder_text = host)
        self.PortEntry.configure(placeholder_text = port)
        
        
#------------------------------------------------MENU----------------------------------------------------------------------------------------------

    def createMenuFrame(self):
        self.menuFrame = customtkinter.CTkFrame(self)
        self.menuFrame.pack()
        self.menuFrame.pack_propagate(False)
        self.menuFrame.configure(width=900, height=600)
        self.menuCanvas = self.createCanvas(self.menuFrame)
        self.menuCanvas.configure(bg=self.bg_color)
        #self.image = ImageTk.PhotoImage(Image.open("Images/board.jpg").resize((900, 600)))
        #self.menuCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.MenuButtons()

    def MenuButtons(self):
        self.menuCanvas.create_text(450, 100, text="Jogo da Velha", font=("Impact", 80), fill = self.text_color)
        self.createGameButton = customtkinter.CTkButton(self.menuCanvas, text="Criar Jogo", text_color= self.text_color,  font=("Impact", 30), command=self.createGameFrame)
        self.menuCanvas.create_window(450, 250, window=self.createGameButton)
        self.joinGameButton = customtkinter.CTkButton(self.menuCanvas, text="Entrar em Jogo", text_color= self.text_color,  font=("Impact", 30), command=self.joinGameFrame)
        self.menuCanvas.create_window(450, 350, window=self.joinGameButton)
        self.joinIAGameButton = customtkinter.CTkButton(self.menuCanvas, text="Entrar em Jogo IA", font=("Impact", 30), text_color=self.text_color, command=self.joinGameIAFrame)
        self.menuCanvas.create_window(450, 450, window=self.joinIAGameButton)
        self.exitButton = customtkinter.CTkButton(self.menuCanvas, text="Sair", text_color= self.text_color , font=("Impact", 30), command=self.destroy)
        self.menuCanvas.create_window(450, 550, window=self.exitButton)
        self.settings_image = ImageTk.PhotoImage(Image.open("Images/settings.png").resize((50, 50)))
        #self.settingsButton = customtkinter.CTkButton(self.menuCanvas, text="Configurações", text_color= self.text_color, font=("Impact", 30),image=self.settings_image, compound="left", command=self.settingsFrame)
        self.settingsButton = customtkinter.CTkButton(self.menuCanvas, text="",image=self.settings_image, command=self.settingsFrame, width=50, height=70)
        self.menuCanvas.create_window(862, 560, window=self.settingsButton)
        if self.loggedIn == False:
            self.profile_image = ImageTk.PhotoImage(Image.open("Images/pessoa2.png").resize((50, 50)))
            self.profileButton = customtkinter.CTkButton(self.menuCanvas, text="", text_color= self.text_color, font=("Impact", 30),image=self.profile_image, compound="left", width=50, height=70, command=self.loginFrame)
            self.menuCanvas.create_window(793, 560, window=self.profileButton)
        else:
            self.profile_image = ImageTk.PhotoImage(Image.open("Images/rank.png").resize((50, 50)))
            self.profileButton = customtkinter.CTkButton(self.menuCanvas, text="", text_color= self.text_color, font=("Impact", 30),image=self.profile_image, compound="left", width=50, height=70, command=self.rankFrame)
            self.menuCanvas.create_window(793, 560, window=self.profileButton)

#------------------------------------------------------LOGIN---------------------------------------------------------------------------------------

    def loginFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.loginPageFrame = customtkinter.CTkFrame(self)
        self.loginPageFrame.pack()
        self.loginPageFrame.pack_propagate(False)
        self.loginPageFrame.configure(width=900, height=600)
        self.loginCanvas = self.createCanvas(self.loginPageFrame)
        self.loginCanvas.configure(bg=self.bg_color)
        #self.profileCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.loginCanvas.create_text(450, 100, text="Login", font=("Impact", 80), fill = self.text_color)
        self.loginButtons()

    def loginButtons(self):
        self.loginCanvas.create_text(450, 200, text="Nome:", font=("Impact", 30), fill = self.text_color)
        self.usrNameEntry = customtkinter.CTkEntry(self.loginCanvas, width=400, font=("Impact", 30))
        self.loginCanvas.create_window(450, 250, window=self.usrNameEntry)
        self.loginCanvas.create_text(450, 300, text="Senha:", font=("Impact", 30), fill = self.text_color)
        self.usrPassEntry = customtkinter.CTkEntry(self.loginCanvas, width=400, font=("Impact", 30))
        self.loginCanvas.create_window(450, 350, window=self.usrPassEntry)
        self.loginButton = customtkinter.CTkButton(self.loginCanvas, text="Entrar", text_color= self.text_color, font=("Impact", 30), command=lambda: self.login("LOGIN"))
        self.loginCanvas.create_window(450, 450, window=self.loginButton)
        self.loginButton = customtkinter.CTkButton(self.loginCanvas, text="Cadastrar", text_color= self.text_color, font=("Impact", 30), command=lambda: self.login("REGIS"))
        self.loginCanvas.create_window(450, 500, window=self.loginButton)
        self.backButton = customtkinter.CTkButton(self.loginCanvas, text="Voltar", text_color= self.text_color, font=("Impact", 30),image=self.back_image,compound= "left", command=lambda: self.backToMenu(self.loginPageFrame))
        self.loginCanvas.create_window(815, 570, window=self.backButton)
        
    def login(self, option):
        self.clickSound()
        self.usrName = self.usrNameEntry.get()
        self.usrPass = self.usrPassEntry.get()
        
        if(len(self.usrName) > 25 or self.usrName == "" or '-' in self.usrName): # Verifica se o nick é invalido(maior que 25 ou vazio)
            messagebox.showinfo("Error", "nick invalido")
            return

        if(len(self.usrPass) > 25 or self.usrPass == "" or '-' in self.usrPass): # Verifica se o nick é invalido(maior que 25 ou vazio)
            messagebox.showinfo("Error", "Senha no formato invalido")
            return
        
        if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
            messagebox.showinfo("Error", "Server is not Running")
            return 

        retorno = sendLoginRegister(self.usrName.ljust(25, "-"), self.usrPass.ljust(25, "-"), option) 
        
        if(retorno == False):
            messagebox.showinfo("Error", "Algo deu errado, tente novamente")
            return
        
        self.loggedIn = True
        self.backToMenu(self.loginPageFrame)


#------------------------------------------------------RANK---------------------------------------------------------------------------------------

    def rankFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.rankPageFrame = customtkinter.CTkFrame(self)
        self.rankPageFrame.pack()
        self.rankPageFrame.pack_propagate(False)
        self.rankPageFrame.configure(width=900, height=600)
        self.rankCanvas = self.createCanvas(self.rankPageFrame)
        self.rankCanvas.configure(bg=self.bg_color)
        #self.profileCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.rankCanvas.create_text(450, 100, text="Rank", font=("Impact", 80), fill = self.text_color)
        self.rankButtons()

    def rankButtons(self):
        if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
            messagebox.showinfo("Error", "Server is not Running")
            self.backToMenu(self.rankPageFrame)
            return 
        
        dataFromUser = getUserStats(self.usrName.ljust(25, "-"))
        print(dataFromUser)
        
        if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
            messagebox.showinfo("Error", "Server is not Running")
            self.backToMenu(self.rankPageFrame)
            return 
        
        dataRank = getRankStats()
        print(dataRank)
                
        self.backButton = customtkinter.CTkButton(self.rankCanvas, text="Voltar", text_color= self.text_color, font=("Impact", 30),image=self.back_image,compound= "left", command=lambda: self.backToMenu(self.rankPageFrame))
        self.rankCanvas.create_window(815, 570, window=self.backButton)

        self.backToMenu(self.rankPageFrame)

#------------------------------------------------------CRIAR JOGO------------------------------------------------------------------------------------

    def createGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.createGamePageFrame = customtkinter.CTkFrame(self)
        self.createGamePageFrame.pack()
        self.createGamePageFrame.pack_propagate(False)
        self.createGamePageFrame.configure(width=900, height=600)
        self.createGameCanvas = self.createCanvas(self.createGamePageFrame)
        self.createGameCanvas.configure(bg=self.bg_color)
        #self.createGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.createGameCanvas.create_text(450, 100, text="Criar Jogo", font=("Impact", 80), fill = self.text_color)
        self.createGameButtons()

    def createGameButtons(self):
        self.createGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = self.text_color)
        
        self.NickEntry = customtkinter.CTkEntry(self.createGameCanvas, font=("Impact", 30), width=400, placeholder_text_color = "#c0c0c0")
        self.createGameCanvas.create_window(450, 250, window=self.NickEntry)
        
        if self.loggedIn == True:
            self.NickEntry.configure(placeholder_text = self.usrName)
            self.NickEntry.configure(state="disabled")
        else:
            self.NickEntry.configure(placeholder_text = 'Entre 1 e 25 caracteres')
            

        def OkCallback():
            if self.loggedIn == False:
                self.nick = self.NickEntry.get() 
            else:
                self.nick = self.usrName
            
            if(len(self.nick) > 25 or self.nick == "" or '-' in self.nick): # Verifica se o nick é invalido(maior que 25 ou vazio)
                messagebox.showinfo("Error", "nick invalido")
                return
            
            if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
                messagebox.showinfo("Error", "Server is not Running")
                return 

            IDVar = createGame(self.nick.ljust(25, "-")) # Manda o nick (com "-" para completar os 25 caracteres) para o servidor e recebe o ID do jogo
            self.waitingRoomGUI(IDVar) # Chama a tela de espera

        self.createGameButton = customtkinter.CTkButton(self.createGameCanvas, text="Criar Jogo", text_color=self.text_color, font=("Impact", 30), command=OkCallback)
        self.createGameCanvas.create_window(450, 400, window=self.createGameButton)

        self.backButton = customtkinter.CTkButton(self.createGameCanvas, text="Voltar", font=("Impact", 30), text_color=self.text_color, image=self.back_image, compound="left", command=lambda: self.backToMenu(self.createGamePageFrame))
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
        self.waitingRoomCanvas.create_text(450, 100, text="Sala de Esperda: ", font=("Impact", 80), fill = self.text_color)
        self.waitingRoomCanvas.create_text(450, 350, text= "ID: " + str(ID), font=("Impact", 40), fill = self.text_color)
        self.waitingRoomCanvas.create_text(450, 450, text= "Esperando Outro Jogador", font=("Impact", 40), fill = self.text_color)

        # self.loading = Image.open("images/loading.gif")
        # self.loadingFrames = []
        # self.loadGifFrames()

        self.eventThread = threading.Event()
        waitingRoomThread = threading.Thread(target=waitingRoom, args=(self.eventThread,)) 
        waitingRoomThread.start()
        
        while not self.eventThread.is_set(): # Fica esperando o outro jogador
            # self.playGif(self.waitingRoomCanvas, self.eventThread, 0)
            self.update()


        print("Jogar")
        self.play(self.waitingRoomPageFrame) # Chama a tela de jogo

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def joinGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.joinGamePageFrame = customtkinter.CTkFrame(self)
        self.joinGamePageFrame.pack()
        self.joinGamePageFrame.pack_propagate(False)
        self.joinGamePageFrame.configure(width=900, height=600)
        self.joinGameCanvas = self.createCanvas(self.joinGamePageFrame)
        self.joinGameCanvas.configure(bg=self.bg_color)
        #self.joinGameCanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGameCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = self.text_color)
        self.joinGameButtons()

    def joinGameButtons(self):
        self.joinGameCanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = self.text_color)
        
        self.NickEntry = customtkinter.CTkEntry(self.joinGameCanvas, font=("Impact", 30), width=400, placeholder_text_color = "#c0c0c0")
        self.joinGameCanvas.create_window(450, 250, window=self.NickEntry)
        
        
        if self.loggedIn == True:
            self.NickEntry.configure(placeholder_text = self.usrName)
            self.NickEntry.configure(state="disabled")
        else:
            self.NickEntry.configure(placeholder_text = 'Entre 1 e 25 caracteres')
            

        def OkCallback():
            if self.loggedIn == False:
                self.nick = self.NickEntry.get() 
            else:
                self.nick = self.usrName      
                  
            if(len(self.nick) > 25 or self.nick == "" or '-' in self.nick): # Verifica se o nick é valido maior que 25 ou vazio
                messagebox.showinfo("Error", "nick invalido")
                return
            
            if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
                messagebox.showinfo("Error", "Server is not Running")
                return 

            joinGame(self.nick.ljust(25, "-")) # Manda o nick (com "-" para completar os 25 caracteres) para o servidor
            self.sendIDGUI() # Chama a tela de mandar o ID

        self.joinGameButton = customtkinter.CTkButton(self.joinGameCanvas, text="Entrar ID", text_color=self.text_color, font=("Impact", 30), command = OkCallback)
        self.joinGameCanvas.create_window(450, 400, window=self.joinGameButton)
        
        self.backButton = customtkinter.CTkButton(self.joinGameCanvas, text="Voltar", font=("Impact", 30), text_color= self.text_color, image=self.back_image, compound="left" , command=lambda: self.backToMenu(self.joinGamePageFrame))
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
        self.SendIDCanvas.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80), fill = self.text_color)
        
        self.SendIDCanvas.create_text(450, 200, text="Escolha ID:", font=("Impact", 30), fill = self.text_color)
        self.IDEntry = customtkinter.CTkEntry(self.SendIDCanvas, font=("Impact", 30), width=400)
        self.SendIDCanvas.create_window(450, 250, window=self.IDEntry)
        
        def OkCallback(rand):
            ID = self.IDEntry.get() # Get the value of the entry field

            if(((not all(digito.isdigit() for digito in ID) and len(ID) != 8) or ID == "") and rand == False): # Verifica se todos os caracteres sao numeros e se o tamanho é 8 e ele nao pode ser vazio
                messagebox.showinfo("Error", "ID invalido")
                return
            
            if rand == True: ID = "--RAND--" 
                
            if sendID(ID) == False: # Verifica se o ID corresponde com o servidor 
                messagebox.showinfo("Error", "ID invalido ou nenhuma sala Vazia")
                return

            print("Jogar")
            self.play(self.joinGamePageFrame) # Chama a tela de jogo
            
        self.joinRandGameButton = customtkinter.CTkButton(self.SendIDCanvas, text="Entrar Rand", text_color=self.text_color, font=("Impact", 30), command=lambda: OkCallback(True))
        self.SendIDCanvas.create_window(550, 400, window=self.joinRandGameButton)
        
        self.SendIDButton = customtkinter.CTkButton(self.SendIDCanvas, text="Entrar", text_color = self.text_color, font=("Impact", 30), command=lambda: OkCallback(False))
        self.SendIDCanvas.create_window(300, 400, window=self.SendIDButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def joinGameIAFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.joinGameIAPageFrame = customtkinter.CTkFrame(self)
        self.joinGameIAPageFrame.pack()
        self.joinGameIAPageFrame.pack_propagate(False)
        self.joinGameIAPageFrame.configure(width=900, height=600)
        self.joinGameIACanvas = self.createCanvas(self.joinGameIAPageFrame)
        self.joinGameIACanvas.configure(bg=self.bg_color)
        #self.joinGameIACanvas.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGameIACanvas.create_text(450, 100, text="Entrar em Jogo IA", font=("Impact", 80), fill = self.text_color)
        self.joinGameIAButtons()

    def joinGameIAButtons(self):
        self.joinGameIACanvas.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30), fill = self.text_color)
        self.NickEntry = customtkinter.CTkEntry(self.joinGameIACanvas, font=("Impact", 30), width=400, placeholder_text = "Entre 1 e 25 caracteres", placeholder_text_color = "#c0c0c0")
        self.joinGameIACanvas.create_window(450, 250, window=self.NickEntry)
        self.joinGameIACanvas.create_text(450, 325, text="Escolha a dificuldade:", font=("Impact", 30), fill = self.text_color)
        self.dificuldade_box = customtkinter.CTkComboBox(self.joinGameIACanvas, values=["", "Iniciante", "Facil", "Intermediário", "Expert"])
        self.joinGameIACanvas.create_window(450, 375, window=self.dificuldade_box)

        def OkCallback():
            
            self.dificuldade = self.dificuldade_box.get()
            self.nick = self.NickEntry.get()
                
            if(self.dificuldade == ""): 
                messagebox.showinfo("Error", "Escolha a dificuldade") 
                return 
                    
            if(len(self.nick) > 25 or self.nick == ""): # Verifica se o nick é valido maior que 25 ou vazio
                messagebox.showinfo("Error", "nick invalido")
                return
            
            if connectToServer(host, port) == False: # Verifica se o servidor esta rodando
                messagebox.showinfo("Error", "Server is not Running")
                return 
            

            dict = {"Iniciante": "0", "Facil": "1", "Intermediário": "2", "Expert": "3"}
            self.dificuldade = dict[self.dificuldade]

            joinGameIA(self.nick.ljust(25, "-"), self.dificuldade) # Manda o nick (com "-" para completar os 25 caracteres) para o servidor
            self.play(self.joinGameIAPageFrame) # Chama a tela de mandar o ID

        self.joinGameButton = customtkinter.CTkButton(self.joinGameIACanvas, text="Entrar", font=("Impact", 30), text_color = self.text_color, command = OkCallback)
        self.joinGameIACanvas.create_window(450, 425, window=self.joinGameButton)
        self.backButton = customtkinter.CTkButton(self.joinGameIACanvas, text="Voltar", font=("Impact", 30), text_color=self.text_color, image=self.back_image, compound="left" , command=lambda: self.backToMenu(self.joinGameIAPageFrame))
        self.joinGameIACanvas.create_window(450, 500, window=self.backButton)

#------------------------------------------------------------------------------------------------------------------------------------------------------

    def resetGameGUI(self):
        for button in self.buttons:
            button.config(text= '', state=DISABLED)

        # self.countDerrotas = 0
        # self.countVitorias = 0
        # self.countEmpates = 0
        
        resetBoad()

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
        self.playCanvas.configure(bg=self.bg_color)
        
        self.playCanvas.create_text(450, 100, text="Jogando", font=("Impact", 80), fill = self.text_color)
        
        self.textoJogarEsperar = self.playCanvas.create_text(450, 180, text="Jogando", font=("Impact", 20), fill= self.text_color)
        self.playCanvas.lift(self.textoJogarEsperar)
        
        self.textoPlacarMeu = self.playCanvas.create_text(200, 300, text="", font=("Impact", 20), fill= self.text_color)
        self.playCanvas.lift(self.textoPlacarMeu)
        
        self.textoPlacarAponente = self.playCanvas.create_text(740, 300, text="", font=("Impact", 20), fill= self.text_color)
        self.playCanvas.lift(self.textoPlacarAponente)

        buttonFrame = Frame(self.playCanvas, width=30, height=15)
        # meio x = 900 (largura do Frame) - 270 (Largura de todos os botões) / 2 = 315
        # meio y = 600 (altura do Frame) - 270 (altura de todos os botões) / 2 = 165
        buttonFrame.place(x=315, y=210) 

        self.img = ImageTk.PhotoImage(Image.open("Images/settings.png").resize((1, 1)))
        
        self.buttons = []
        for i in range(9):
            button = Button(buttonFrame, width=85, height=85, command=lambda i=i: self.turnPlay(i), state=DISABLED, font="cmr 80 bold", image=self.img, compound="left", bg= self.bg_color, activebackground = self.bg_color, borderwidth=2)
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
        
        self.playPageFrame.place(x=0, y=0)

        self.backButton = Button(self.playCanvas, text="Sair", font=("Impact", 30), command = self.destroy)
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
        
        self.simboloInt = getSimbolo() # Recebe o simbolo do jogador, 0 ou 1 (X ou O)
        self.nickOponente = getNickOponente().replace('-', '') # Recebe o nick do oponente e remove os traços
        print("nickOponente: " + self.nickOponente)
        sendLoginState(self.loggedIn)
        
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

                self.playCanvas.itemconfig(self.textoPlacarMeu, 
                                           text = "Voce → " + simbolos[self.simboloInt] + "\n" + 
                                          "Nome → " + self.nick + "\n" + 
                                          "pts → " + str(self.countVitorias), 
                                          fill = corSimbulos[self.simboloInt]) # Atualiza o placar do jogador
                
                self.playCanvas.itemconfig(self.textoPlacarAponente, 
                                           text = simbolos[1 - self.simboloInt] + " ← Oponente" + "\n" + 
                                           self.nickOponente + " ← Nome" + "\n" + 
                                           str(self.countDerrotas) + " ← pts", 
                                           fill = corSimbulos[1 - self.simboloInt]) # Atualiza o placar do oponente

                time.sleep(2)

                print("TURNO: " + self.turn)

                if self.turn == 'PLAY': 
                    self.playCanvas.itemconfig(self.textoJogarEsperar, text="SEU TURNO. JOGUE") # Atualiza o texto de jogar ou esperar
                    board = getBoard()
                    for i, button in enumerate(self.buttons): # Passa por todos os botoes
                        if board[i//3][i%3] == '': # Se o botao estiver vazio
                            button.config(state=NORMAL) # Ativa o botao

                    self.wait_variable(self.buttonPressed) # Esperar por um botao ser pressionado

                elif self.turn == 'WAIT':
                    self.playCanvas.itemconfig(self.textoJogarEsperar, text="TRUNO DO OPODENTE. ESPERE") # Atualiza o texto de jogar ou esperar
                    self.turnWait()

                else:
                    raise Exception

        except Exception:
            self.playing = False
            self.quit()

    def endGameGUI(self):
        self.playCanvas.itemconfig(self.textoJogarEsperar, text="ESPERANDO RESPOSTA PARA REINICIAR O JOGO")
        response = messagebox.askyesno("Fim do jogo", "Reiniciar o jogo?") # Pergunta se o jogador quer jogar novamente

        event = threading.Event()
        fileResultado = Queue()
        endGameDecideThread = threading.Thread(target=endGameDecide, args=(response, event, fileResultado)) # Cria uma thread para decidir se o jogo vai ser reiniciado ou não
        endGameDecideThread.start()

        while not event.wait(1): # Espera a thread terminar
            self.update()

        self.playing = not fileResultado.get() # Se o jogo não for reiniciado, a variavel playing é setada para False

        if(self.playing == True): # Se o jogo for reiniciado
            print("Reset GUI")
            self.resetGameGUI()
        else: # Se o jogo não for reiniciado
            print("Fim Game GUI")
            endGame()
            self.destroy()

    def updateGui(self, message, simbolo):
        if message == "WIN":
            print("WIN")
            printBoard()
            position = recvGameState(simbolo)
            self.buttons[position].config(text=simbolos[simbolo], state=DISABLED, disabledforeground = corSimbulos[simbolo])
            pygame.mixer.pause()
            music_win = pygame.mixer.Sound("Sounds/vitoria.wav")
            music_win.play()
            messagebox.showinfo("Fim do Jogo", "Voce Ganhou")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
            pygame.mixer.unpause()
            self.countVitorias += 1
            
        if message == "DEF":
            print("DEF")
            printBoard()
            position = recvGameState(simbolo)
            self.buttons[position].config(text=simbolos[simbolo], state=DISABLED, disabledforeground = corSimbulos[simbolo])
            pygame.mixer.pause()
            music_loss = pygame.mixer.Sound("Sounds/derrota.mp3")
            music_loss.play()
            messagebox.showinfo("Fim do Jogo", "Voce Perdeu")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
            pygame.mixer.unpause()
            self.countDerrotas += 1
        
        elif message == "TIE":
            print("TIE")
            printBoard()
            position = recvGameState(simbolo)
            self.buttons[position].config(text=simbolos[simbolo], state=DISABLED, disabledforeground = corSimbulos[simbolo])
            pygame.mixer.pause()
            self.music_tie = pygame.mixer.Sound("Sounds/empate.mp3")
            self.music_tie.play()
            messagebox.showinfo("Fim do Jogo", "Jogo Empatado")
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
            pygame.mixer.unpause()
            self.countEmpates += 1
        
        elif message == "VAL":
            print("VAL")
            printBoard()
            position = recvGameState(simbolo)
            self.buttons[position].config(text=simbolos[simbolo], state=DISABLED, disabledforeground = corSimbulos[simbolo])
        
        elif message == "INV":
            print("INV")
            self.quit()

        if message in ["DEF", "TIE", "WIN"]:
            self.endGameGUI()
    
    def turnWait(self):
        try:
            # self.loading = Image.open("images/loading.gif")
            # self.loadingFrames = []
            # self.loadGifFrames()
            
            for i, button in enumerate(self.buttons): # Passa por todos os botoes
                button.config(state=DISABLED) # Desativa o botao

            fileResultado = Queue()
            event = threading.Event()
            waitingRoomThread = threading.Thread(target=waitResponse, args=(event, fileResultado,)) # Cria uma thread para esperar a resposta do servidor
            waitingRoomThread.start()
            
            while not event.is_set():
                # self.playGif(self.playCanvas, event, 0)
                self.update()
            
            message = fileResultado.get() # Pega a mensagem recebida do servidor na thread

            self.updateGui(message, 1-self.simboloInt) # Atualiza a GUI com a mensagem recebida do servidor
            

        except:
            print("Trun Wait Error")
            self.playing = False
            
    def turnPlay(self, i):
        
        posicoes = ["11", "12", "13", "21", "22", "23", "31", "32", "33"]
        
        # for i, button in enumerate(self.buttons): # Passa por todos os botoes
        #         button.config(state=DISABLED) # Desativa o botao
        
        try:
            message = sendMove(posicoes[i]) # Envia a jogada para o servidor

            self.updateGui(message, self.simboloInt) # Atualiza a GUI com a mensagem recebida do servidor

            self.buttonPressed.set(True) # Seta a variavel buttonPressed para True para que o loop principal posso continuar 

        except:
            self.quit()
        

if __name__ == "__main__":
    client = ClientGUI()
    client.mainloop()
    sys.exit()

