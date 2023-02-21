import tkinter as tk
import sys
import os

client_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(client_dir)
from client import *

# Create the main window
window = tk.Tk()
window.title("My GUI")

# Create the label for the title
title_label = tk.Label(window, text="Welcome to my GUI!", font=("Arial", 24))
title_label.pack(pady=20) # Add some padding to the top

def resetWindow():
    for item in window.winfo_children():
        item.destroy()

def join_game():
    resetWindow()

    # Create a new window for entering the variable
    # window = tk.Toplevel(window)
    window.title("Join Game")

    # Create a label and entry field for the variable
    var_label = tk.Label(window, text="Enter a string:")
    var_entry = tk.Entry(window)

    # Add the label and entry field to the window
    var_label.pack(pady=10)
    var_entry.pack(pady=10)

    # Create a callback function for the "OK" button
    def ok_callback():
        var = var_entry.get() # Get the value of the entry field
        joinGame() # Call the joinGame function with the entered variable
        window.destroy() # Close the window

    # Create an "OK" button to submit the variable
    ok_button = tk.Button(window, text="OK", command=ok_callback)
    ok_button.pack(pady=10)

def create_game():
    resetWindow()
    # Create a new window for entering the variable
    # window = tk.Toplevel(window)
    window.title("Create Game")

    # Create a label and entry field for the variable
    var_label = tk.Label(window, text="Enter a string:")
    var_entry = tk.Entry(window)

    # Add the label and entry field to the window
    var_label.pack(pady=10)
    var_entry.pack(pady=10)

    # Create a callback function for the "OK" button
    def ok_callback():
        var = var_entry.get() # Get the value of the entry field
        #ir para uma sala de espera (tela nova)
        createGame() # Call the createGame function with the entered variable
        window.destroy() # Close the window

    # Create an "OK" button to submit the variable
    ok_button = tk.Button(window, text="OK", command=ok_callback)
    ok_button.pack(pady=10)

# Create the two buttons
button1 = tk.Button(window, text="Join", command=join_game)
button2 = tk.Button(window, text="Create", command=create_game)

# Add the buttons to the window
button1.pack(side="left", padx=20)
button2.pack(side="right", padx=20)

# Start the GUI
window.mainloop()