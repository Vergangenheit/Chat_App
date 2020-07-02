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
        client.send(bytes(name, "utf8") + msg)


def client_communication(person):
    client = person.client

    # first message received is always the person name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")
    run = True
    while True:  # wait for nay messages from person
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))
            # if we receive a message we have to broadcast it to all of our clients
            if msg == bytes("{quit}", "utf8"):  # if message is quit, disconnect disconnect client
                # client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """Wait infinitely for connections from incoming clients
   Start new thread once connected"""
    while True:
        try:
            client, addr = SERVER.accept()  # wait for nay new connections
            person = Person(addr, client) # create new person for connection
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()

        except Exception as e:
            print("[FAILURE]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for connections.
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
