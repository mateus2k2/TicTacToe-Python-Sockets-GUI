import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Grid of Buttons")

# Create the main frame
main_frame = tk.Frame(root)
main_frame.pack()

# Create the smaller frame for the buttons
button_frame = tk.Frame(main_frame)
button_frame.pack()

# Create the buttons in a loop
for row in range(3):
    for column in range(3):
        # Create the button and add it to the grid
        button = tk.Button(button_frame, text=f"Button {row+1}-{column+1}")
        button.grid(row=row, column=column, padx=5, pady=5)

# Start the main loop
root.mainloop()