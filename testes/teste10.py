import tkinter as tk

class FadedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder_text = self.cget("text")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.fade_in()

    def fade_in(self):
        self.configure(text=self.placeholder_text, foreground="gray50")
        self.after(500, self.fade_out)

    def fade_out(self):
        self.configure(text=self.placeholder_text, foreground="gray70")
        self.after(500, self.fade_in)

    def on_enter(self, event):
        self.fade_out()

    def on_leave(self, event):
        self.fade_in()

# Example usage:
root = tk.Tk()
btn = FadedButton(root, text="Click me")
btn.pack()
root.mainloop()