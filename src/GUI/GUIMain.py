from tkinter import *
from PIL import ImageTk, Image
import pygame

class ClientGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Velha")
        self.geometry("900x600")
        self.resizable(False, False)
        pygame.mixer.init()
        self.play_music()
        self.createMenuFrame()
# Cria a tela do Menu
    def createMenuFrame(self):
        self.menuFrame = Frame(self)
        self.menuFrame.pack()
        self.menuFrame.pack_propagate(False)
        self.menuFrame.configure(width=900, height=600)
        self.menu = self.createCanvas(self.menuFrame)
        self.create_images()
        self.menu.create_image(0, 0, image=self.image, anchor=NW)
        self.MenuButtons()
# Abre a imagem da tela de fundo
    def create_images(self):
        self.image = ImageTk.PhotoImage(Image.open("Images/board.jpg").resize((900, 600), Image.ANTIALIAS))
# Cria e retorna um canvas para ser usado em cada tela
    def createCanvas(self, master):
        canvas = Canvas(master, width=900, height=600)
        canvas.pack()
        return canvas
# Cria e adiciona os botões da tela de menu -> Criar Jogo, Entrar em jogo, Sair e Configurações
    def MenuButtons(self):
        self.menu.create_text(450, 100, text="Jogo da Velha", font=("Impact", 80))
        self.createGameButton = Button(self.menu, text="Criar Jogo", font=("Impact", 30), command=self.createGameFrame)
        self.menu.create_window(450, 300, window=self.createGameButton)
        self.joinGameButton = Button(self.menu, text="Entrar em Jogo", font=("Impact", 30), command=self.joinGameFrame)
        self.menu.create_window(450, 400, window=self.joinGameButton)
        self.exitButton = Button(self.menu, text="Sair", font=("Impact", 30), command=self.destroy)
        self.menu.create_window(450, 500, window=self.exitButton)
        self.settingsButton = Button(self.menu, text="Configurações", font=("Impact", 30), command=self.settingsFrame)
        self.menu.create_window(775, 570, window=self.settingsButton)
# Da play na musica logo quando a tela raiz é criada
    def play_music(self):
        self.music = pygame.mixer.Sound("Sounds/Music.wav")
        self.music.set_volume(0.2)
        self.music.play(-1)
# Da play no som de clique
    def clickSound(self):
        click = pygame.mixer.Sound("Sounds/click.wav")
        click.play()
# Cria a tela de Criar jogo
    def createGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.createGamePage = Frame(self)
        self.createGamePage.pack()
        self.createGamePage.pack_propagate(False)
        self.createGamePage.configure(width=900, height=600)
        self.createGame = self.createCanvas(self.createGamePage)
        self.createGame.create_image(0, 0, image=self.image, anchor=NW)
        self.createGame.create_text(450, 100, text="Criar Jogo", font=("Impact", 80))
        self.createGameButtons()
# Define os botões e box de entrada da tela de criar jogo
    def createGameButtons(self):
        self.createGame.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30))
        self.gameNameEntry = Entry(self.createGame, font=("Impact", 30), width=20)
        self.createGame.create_window(450, 250, window=self.gameNameEntry)
        self.createGameButton = Button(self.createGame, text="Criar Jogo", font=("Impact", 30))
        self.createGame.create_window(450, 400, window=self.createGameButton)
        self.backButton = Button(self.createGame, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.createGamePage))
        self.createGame.create_window(450, 500, window=self.backButton)
# Cria a tela de Entrar no Jogo
    def joinGameFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.joinGamePage = Frame(self)
        self.joinGamePage.pack()
        self.joinGamePage.pack_propagate(False)
        self.joinGamePage.configure(width=900, height=600)
        self.joinGame = self.createCanvas(self.joinGamePage)
        self.joinGame.create_image(0, 0, image=self.image, anchor=NW)
        self.joinGame.create_text(450, 100, text="Entrar em Jogo", font=("Impact", 80))
        self.joinGameButtons()
# Botões e caixas de entrada de Entrar no jogo
    def joinGameButtons(self):
        self.joinGame.create_text(450, 200, text="Escolha seu Nick:", font=("Impact", 30))
        self.gameNameEntry = Entry(self.joinGame, font=("Impact", 30), width=20)
        self.joinGame.create_window(450, 250, window=self.gameNameEntry)
        self.joinGame.create_text(450, 300, text="Digite o ID:", font=("Impact", 30))
        self.gameNameEntry = Entry(self.joinGame, font=("Impact", 30), width=20)
        self.joinGame.create_window(450, 350, window=self.gameNameEntry)
        self.joinGameButton = Button(self.joinGame, text="Entrar", font=("Impact", 30))
        self.joinGame.create_window(450, 400, window=self.joinGameButton)
        self.backButton = Button(self.joinGame, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.joinGamePage))
        self.joinGame.create_window(450, 500, window=self.backButton)
# Cria a tela de configurações
    def settingsFrame(self):
        self.clickSound()
        self.menuFrame.destroy()
        self.settingsPage = Frame(self)
        self.settingsPage.pack()
        self.settingsPage.pack_propagate(False)
        self.settingsPage.configure(width=900, height=600)
        self.settings = self.createCanvas(self.settingsPage)
        self.settings.create_image(0, 0, image=self.image, anchor=NW)
        self.settings.create_text(450, 100, text="Configurações", font=("Impact", 80))
        self.settingsButtons()
# botão voltar e definir o som em configurações
    def settingsButtons(self):
        self.settings.create_text(450, 200, text="Configurações", font=("Impact", 30))
        self.volume = Scale(self.settings, from_=0, to=100, orient=HORIZONTAL, length=300, font=("Impact", 30), command=lambda x: self.music.set_volume(int(x)/100))
        self.settings.create_window(450, 300, window=self.volume)
        self.backButton = Button(self.settings, text="Voltar", font=("Impact", 30), command=lambda: self.backToMenu(self.settingsPage))
        self.settings.create_window(450, 500, window=self.backButton)
# Implementação do botão voltar -> destrói a pagina atual e cria uma nova pagina de Menu
    def backToMenu(self, page):
        self.clickSound()
        page.destroy()
        self.createMenuFrame()





if __name__ == "__main__":
    client = ClientGUI()
    client.mainloop()
