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
from server import *

simbolos = ['X', 'O']

class ServerGUI(Tk):
    def __init__(self):
        pass

        

if __name__ == "__main__":
    client = ServerGUI()
    client.mainloop()
    sys.exit()

