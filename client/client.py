from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    for comminucation with server
    """
    BUFSIZ = 512
    HOST = 'localhost'
    PORT = 5500
    ADDR = (HOST, PORT)

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                print(msg)
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        returns a list of str messages
        :return: list[str]
        """
        self.lock.acquire()
        self.lock.release()
        return self.messages

    def disconnect(self):
        self.send_message(bytes("{quit}", "utf8"))
