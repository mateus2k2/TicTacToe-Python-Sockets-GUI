import tkinter as tk
from tkinter import messagebox
import sys
import os

client_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(client_dir)
from client import *

# Create the main window
window = tk.Tk()

canvas = tk.Canvas(window)
canvas.pack()

# mainFrame = canvas.create_text(100, 100, text="mainFrame")
# joinFrame = canvas.create_text(100, 100, text="joinFrame")
# createFrame = canvas.create_text(100, 100, text="createFrame")
# waintingFrame = canvas.create_text(100, 100, text="waintingFrame")
# IDFrame = canvas.create_text(100, 100, text="IDFrame")

# canvas.itemconfig(mainFrame, state="hidden")
# canvas.itemconfig(joinFrame, state="hidden")
# canvas.itemconfig(createFrame, state="hidden")
# canvas.itemconfig(waintingFrame, state="hidden")
# canvas.itemconfig(IDFrame, state="hidden")

# mainFrame = tk.Frame(window)
# joinFrame = tk.Frame(window)
# createFrame = tk.Frame(window)
# waintingFrame = tk.Frame(window)
# IDFrame = tk.Frame(window)

def mainWindow():
    # joinFrame.destroy()
    # createFrame.destroy()
    # waintingFrame.destroy()
    # IDFrame.destroy()

    # mainFrame.pack()

    # title_label = tk.Label(mainFrame, text="TicTacToe", font="Helvetica 16 bold")
    # title_label.pack(side=tk.TOP, fill=tk.X)
    # mainFrame.pack()
    
    mainFrame = tk.Toplevel(window)
    mainFrame.title("My Window Title")

    # Create the two buttons
    button1 = tk.Button(mainFrame, text="Join", command=join_game)
    button2 = tk.Button(mainFrame, text="Create", command=create_game)

    # Add the buttons to the window
    button1.pack(side="left", padx=20)
    button2.pack(side="right", padx=20)

def join_game():
    # createFrame.destroy()
    # mainFrame.destroy()
    # waintingFrame.destroy()
    # IDFrame.destroy()

    # joinFrame.pack()

    # title_label = tk.Label(joinFrame, text="Join a game", font="Helvetica 16 bold")
    # title_label.pack(side=tk.TOP, fill=tk.X)
    # joinFrame.pack()

    joinFrame = tk.Toplevel(window)
    joinFrame.title("My Window Title")

    nickLabel = tk.Label(joinFrame, text="Enter you Nickname:")
    nickEntry = tk.Entry(joinFrame)
    nickLabel.pack(pady=10)
    nickEntry.pack(pady=10)

    IPLabel = tk.Label(joinFrame, text="Enter the server IP:")
    IPEntry = tk.Entry(joinFrame)
    IPLabel.pack(pady=10)
    IPEntry.pack(pady=10)

    PortLabel = tk.Label(joinFrame, text="Enter server Port:")
    PortEntry = tk.Entry(joinFrame)
    PortLabel.pack(pady=10)
    PortEntry.pack(pady=10)

    # Create a callback function for the "OK" button
    def OkCallback():
        nick = nickEntry.get() # Get the value of the entry field
        IP = IPEntry.get() # Get the value of the entry field
        Port = PortEntry.get() # Get the value of the entry field

        if connectToServer(IP, int(Port)) == False:
            messagebox.showinfo("Error", "Server is not Running")
            return 

        joinGame(nick) # Call the joinGame function with the entered variable

        send_ID()

        # joinFrame.destroy() # Close the window

    # Create an "OK" button to submit the variable
    OkButton = tk.Button(joinFrame, text="OK", command=OkCallback)
    OkButton.pack(pady=10)

def send_ID():
    # createFrame.destroy()
    # mainFrame.destroy()
    # waintingFrame.destroy()
    # joinFrame.destroy()

    # IDFrame.pack()

    # title_label = tk.Label(IDFrame, text="ID", font="Helvetica 16 bold")
    # title_label.pack(side=tk.TOP, fill=tk.X)
    # IDFrame.pack()
    
    IDFrame = tk.Toplevel(window)

    IDLabel = tk.Label(IDFrame, text="Enter the Room ID:")
    IDEntry = tk.Entry(IDFrame)
    IDLabel.pack(pady=10)
    IDEntry.pack(pady=10)

    # Create a callback function for the "OK" button
    def OkCallback():
        ID = IDEntry.get() # Get the value of the entry field

        if sendID(ID) == False:
            messagebox.showinfo("Error", "Room is not Available")
            return

        # jogar()

        IDFrame.destroy() # Close the IDFrame

    # Create an "OK" button to submit the variable
    OkButton = tk.Button(IDFrame, text="OK", command=OkCallback)
    OkButton.pack(pady=10)

def waiting_Room(ID):
    # createFrame.destroy()
    # mainFrame.destroy()
    # IDFrame.destroy()
    # joinFrame.destroy()

    # waintingFrame = tk.Frame(window)
    # waintingFrame.pack()

    # title_label = tk.Label(waintingFrame, text="ID", font="Helvetica 16 bold")
    # title_label.pack(side=tk.TOP, fill=tk.X)
    # waintingFrame.pack()

    waintingFrame = tk.Toplevel(window)

    # Create a new window for entering the variable
    # window = tk.Toplevel(window)
    window.title("Waiting Room")

    label = tk.Label(waintingFrame, text="ID: " + ID + " - Waiting for another player...")
    label.pack()

    if waitingRoom() == True:
        # jogar()
        messagebox.showinfo("OK", "Jogador Conectado")
        
def create_game():
    # joinFrame.destroy()
    # mainFrame.destroy()
    # waintingFrame.destroy()
    # IDFrame.destroy()

    # createFrame = tk.Frame(window)
    # createFrame.pack()

    # title_label = tk.Label(createFrame, text="Host a game", font="Helvetica 16 bold")
    # title_label.pack(side=tk.TOP, fill=tk.X)
    # createFrame.pack()

    createFrame = tk.Toplevel(window)

    nickLabel = tk.Label(createFrame, text="Enter you Nickname:")
    nickEntry = tk.Entry(createFrame)
    nickLabel.pack(pady=10)
    nickEntry.pack(pady=10)

    IPLabel = tk.Label(createFrame, text="Enter the server IP:")
    IPEntry = tk.Entry(createFrame)
    IPLabel.pack(pady=10)
    IPEntry.pack(pady=10)

    PortLabel = tk.Label(createFrame, text="Enter server Port:")
    PortEntry = tk.Entry(createFrame)
    PortLabel.pack(pady=10)
    PortEntry.pack(pady=10)

    # Create a callback function for the "OK" button
    def OkCallback():
        nick = nickEntry.get() # Get the value of the entry field
        IP = IPEntry.get() # Get the value of the entry field
        Port = PortEntry.get() # Get the value of the entry field

        if connectToServer(IP, int(Port)) == False:
            messagebox.showinfo("Error", "Server is not Running")
            return 

        #ir para uma sala de espera (tela nova)
        createGame(nick) # Call the createGame function with the entered variable

        waiting_Room(ID)

        # waintingFrame.destroy() # Close the window

    # Create an "OK" button to submit the variable
    OkButton = tk.Button(createFrame, text="OK", command=OkCallback)
    OkButton.pack(pady=10)

mainWindow()

# Start the GUI
window.mainloop()