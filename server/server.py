from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

"""we're going two have two threads, 
1- waiting for new connections, 
2- waiting for new messages"""

# GLOBAL CONSTANTS
BUFSIZ = 512
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server


def broadcast(msg, name):
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    client = person.client
    name = person.name
    addr = person.addr

    # get person name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = f"{name} has joined the chat!"
    broadcast(msg)
    while True:
        msg = client.recv(BUFSIZ)
        # if we receive a message we have to broadcast it to all of our clients
        if msg == bytes("{quit}", "utf8"):
            broadcast(f"{name} has left the chat...", "")
            client.send(bytes("{quit}", "utf8"))
            client.close()
            persons.remove(person)
        else:
            client.send(msg, name)

    # if we receive a message we have to broadcast it to all of our clients


def wait_for_connection(SERVER):
    """Wait infinitely for connections from incoming clients
   Start new thread once connected"""
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()

        except Exception as e:
            print("[FAILURE]", e)
            run = False

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
