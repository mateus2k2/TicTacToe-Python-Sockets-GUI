import customtkinter as tk

# Define the list of dictionaries
data = [
    {'Name': 'John', 'Age': 30, 'City': 'New York'},
    {'Name': 'Sarah', 'Age': 25, 'City': 'London'},
    {'Name': 'Bob', 'Age': 35, 'City': 'Paris'}
]

# Create a Treeview widget with columns
table = tk.Treeview(columns=['Name', 'Age', 'City'])

# Set column headings
table.heading('#0', text='Index')
table.heading('#1', text='Name')
table.heading('#2', text='Age')
table.heading('#3', text='City')

# Insert data into the treeview
for i, row_data in enumerate(data):
    name = row_data['Name']
    age = row_data['Age']
    city = row_data['City']
    table.insert(parent='', index='end', text=i+1, values=(name, age, city))

# Pack the table widget
table.pack()

# Start the main event loop
tk.mainloop()
