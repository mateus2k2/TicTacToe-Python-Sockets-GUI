import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.buttons = []

        for i in range(9):
            button = tk.Button(self.master, width=10, height=5, command=lambda i=i: self.clicked(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def clicked(self, i):
        if self.board[i] == "":
            self.board[i] = self.current_player
            self.buttons[i].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"{self.current_player} wins!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_patterns = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != "":
                return True
        return False

    def reset_game(self):
        self.current_player = "X"
        self.board = ["", "", "", "", "", "", "", "", ""]
        for button in self.buttons:
            button.config(text="")

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()