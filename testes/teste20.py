from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Load the image
img = ImageTk.PhotoImage(Image.open("src/GUI/images/back.png").resize((1, 1)))

# Create the button
button = Button(root, text="X", compound="left", image=img, fg="#EE4035", font="cmr 80 bold", width=85, height=85)

button.config(text="O", state=DISABLED, fg="#EE4035", disabledforeground="#EE4035")


# Show the button
button.pack()

root.mainloop()