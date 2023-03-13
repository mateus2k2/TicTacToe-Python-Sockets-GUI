import tkinter as tk
from tkinter.font import Font

# Create a new Tkinter window
window = tk.Tk()

# Create a new font object from a TTF file
font_path = "impact.ttf"
custom_font = Font(family="My Custom Font", size=30, name=font_path)

# Create a new label widget and set its font
label = tk.Label(window, text="Hello, world!", font=custom_font)
label.pack()

# Run the Tkinter event loop
window.mainloop()