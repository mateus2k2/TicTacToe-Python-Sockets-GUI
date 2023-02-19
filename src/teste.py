# Define a list of dictionaries
my_list = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 40}]

# Use a list comprehension and the next() function to find the first dictionary with name 'Alice'
alice_dict = next((d for d in my_list if d['name'] == 'Alice'), None)

# Print the resulting dictionary
print(alice_dict)