import socket
import select

HOST = ''  # server address
PORT = 12345  # server port
MAX_MSG_SIZE = 1024  # maximum message size

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen(2)

# accept the first client connection
print("Waiting for the first client to connect...")
client1_socket, client1_address = server_socket.accept()
print(f"First client connected from {client1_address}")

# accept the second client connection
print("Waiting for the second client to connect...")
client2_socket, client2_address = server_socket.accept()
print(f"Second client connected from {client2_address}")

# wait for messages from both clients
print("Waiting for messages from both clients...")
while True:
    # create a list of sockets to wait for events
    read_sockets = [client1_socket, client2_socket]
    
    # wait for events using select
    read_ready, write_ready, exception_ready = select.select(read_sockets, [], [])
    
    # handle events for each socket
    for sock in read_ready:
        if sock == client1_socket:
            message = sock.recv(MAX_MSG_SIZE).decode()
            if message:
                print(f"Received message from the first client: {message}")
        elif sock == client2_socket:
            message = sock.recv(MAX_MSG_SIZE).decode()
            if message:
                print(f"Received message from the second client: {message}")
    
    # check if both clients have sent messages
    if client1_socket._closed or client2_socket._closed:
        print("One of the clients has disconnected.")
        break
    elif client1_socket.recv(MAX_MSG_SIZE) == b'' and client2_socket.recv(MAX_MSG_SIZE) == b'':
        print("Both clients have disconnected.")
        break

# close the sockets
client1_socket.close()
client2_socket.close()
server_socket.close()