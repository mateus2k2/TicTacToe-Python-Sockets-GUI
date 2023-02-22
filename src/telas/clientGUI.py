from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import pygame
from pygame.mixer import Sound
pygame.mixer.init()
class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.iconbitmap("Images/icon.ico")
        pygame.mixer.music.load("telas/Sounds/Music.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.my_canvas = Canvas(self.root, width=900, height=600)
        self.my_canvas.pack(fill="both", expand=True)
        img = Image.open("telas/Images/Board.jpg")
        img = img.resize((900, 600), Image.ANTIALIAS)
        imaga = ImageTk.PhotoImage(img)
        self.escolha = -1
        self.ID = ""
        self.my_canvas.create_image(0, 0, image=imaga, anchor="nw")
        #self.my_canvas.create_text((900/2), (600/6), text="Jogo da Velha", font=("Impact", 80), fill="#d1d1d1")
        self.createGame = tk.Button(self.root, text="Criar Jogo", font=("Impact", 20), bg="white", fg="black", width=15, height=2, command= self.escolhaCriar)
        self.createGame_window = self.my_canvas.create_window(450, 240, anchor="center", window=self.createGame)
        self.joinGame = tk.Button(self.root, text="Entrar em Jogo", font=("Impact", 20), bg="white", fg="black", width=15, height=2, command=self.escolhaJoin)
        self.joinGame_window = self.my_canvas.create_window(450, 370, anchor="center", window=self.joinGame)
        self.exitGame = tk.Button(self.root, text="Sair", font=("Impact", 20), bg="white", fg="black", width=15, height=2, command=self.root.destroy)
        self.exitGame_window = self.my_canvas.create_window(450, 500, anchor="center", window=self.exitGame)
        self.imagem = Image.open("telas/Images/settings.png")
        self.imagem = self.imagem.resize((50, 50), Image.ANTIALIAS)
        self.imagem = ImageTk.PhotoImage(self.imagem)
        self.settings = tk.Button(self.root, width=10, height=10, image=self.imagem, command=lambda: print("teste"))
        self.settings_window = self.my_canvas.create_window(850, 550, anchor="center", window=self.settings)
        self.volume_Scale = tk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=100, width=10, command=lambda x: pygame.mixer.music.set_volume(int(x)/100))
        self.volume_Scale_window = self.my_canvas.create_window(850, 500, anchor="center", window=self.volume_Scale)
        self.text_box = tk.Entry(self.root, width=10, font=("Impact", 20))
        self.text_box_window = self.my_canvas.create_window(850, 450, anchor="center", window=self.text_box)
        self.texto = ""
        self.getTextButton = tk.Button(self.root, text="Get Text", command= self.getTextBox)
        self.getTextButton_window = self.my_canvas.create_window(850, 400, anchor="center", window=self.getTextButton)

        self.root.mainloop()
    def getTextBox(self):
        self.texto = self.text_box.get()
    def escolhaCriar(self):
        self.escolha = 1
        self.printaID()
    def escolhaJoin(self):
        self.escolha = 0
    def printaID(self):
        self.my_canvas.create_text((900/2), (600/6), text="ID:" + self.ID, font=("Impact", 80), fill="#d1d1d1")


#def redimensionar(event):
#    global img1, img_redimensionada, nova_img
#    img1 = Image.open("./images/board.jpg")
#    img_redimensionada = img1.resize((event.width, event.height), Image.ANTIALIAS)
#    nova_img = ImageTk.PhotoImage(img_redimensionada)
#    my_canvas.create_image(0, 0, image=nova_img, anchor="nw")
#    my_canvas.create_text((event.width/2), (event.height/6), text="Jogo da Velha", font=("Impact", 80), fill="#d1d1d1")
#    my_canvas.coords(createGame_window, (event.width * 0.5), (event.height * 0.5))
#    my_canvas.itemconfigure(createGame_window, width=(event.width/4.5), height=(event.height/10), anchor="center")
#    #my_canvas.coords(joinGame_window, (event.width/2), (event.height * 0.6))
    #my_canvas.itemconfigure(joinGame_window, width=(event.width/4.5), height=(event.height/9.5), anchor="center")
    #my_canvas.coords(exitGame_window, (event.width/2), (event.height/1.2))
    #my_canvas.itemconfigure(exitGame_window, width=(event.width/4.5), height=(event.height/9.5), anchor="center")

#root.bind('<Configure>', redimensionar)

root = Tk()
ClientGUI(root)