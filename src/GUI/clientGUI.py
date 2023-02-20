import tkinter as tk

# create a function to handle the input
def handle_input():
    input_text = input_field.get()
    print(f"User input: {input_text}")
    input_field.delete(0, tk.END)

# create the GUI
root = tk.Tk()

# create a label for the input field
input_label = tk.Label(root, text="Enter your input:")
input_label.pack()

# create the input field
input_field = tk.Entry(root)
input_field.pack()

# create a button to submit the input
submit_button = tk.Button(root, text="Submit", command=handle_input)
submit_button.pack()

# start the main event loop
root.mainloop()
