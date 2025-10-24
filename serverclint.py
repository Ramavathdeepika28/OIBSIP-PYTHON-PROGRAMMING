import socket     
import threading

# Define the IP address and port for the chat
HOST = '127.0.0.1'  # Localhost (your own computer)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def listen_for_messages(connection):
    """
    This function runs in a background thread to constantly
    listen for incoming messages and print them.
    """
    while True:
        try:
            data = connection.recv(1024)  # Receive up to 1024 bytes
            if not data:
                print("\nThe other side has closed the connection.")
                break
            print("\nReceived:", data.decode())
        except:
            # Something went wrong, probably connection lost
            break

def run_server():
    """
    Set up the server socket, wait for a client to connect,
    then let both sides send and receive messages.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Bind to address and port
        server_socket.listen()  # Start listening for incoming connections
        print(f"Server is listening on {HOST}:{PORT}. Waiting for a client to connect...")

        conn, addr = server_socket.accept()  # Accept a connection
        print(f"Connected by {addr}")

        # Start the thread to listen for messages from client
        threading.Thread(target=listen_for_messages, args=(conn,), daemon=True).start()

        # Main thread: sending messages to client
        while True:
            msg = input("You: ")
            if msg.lower() == 'exit':
                print("Closing connection...")
                break
            conn.sendall(msg.encode())  # Send the message

def run_client():
    """
    Connect to the server, then send and receive messages.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Connect to the server
        print(f"Connected to server at {HOST}:{PORT}")

        # Start the thread to listen for messages from server
        threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True).start()

        # Main thread: sending messages to server
        while True:
            msg = input("You: ")
            if msg.lower() == 'exit':
                print("Closing connection...")
                break
            client_socket.sendall(msg.encode())

if __name__ == "__main__":
    mode = input("Do you want to run as server (s) or client (c)? ").strip().lower()
    if mode == 's':
        run_server()
    elif mode == 'c':
        run_client()
    else:
        print("Invalid choice. Please run the program again and enter 's' or 'c'.")
