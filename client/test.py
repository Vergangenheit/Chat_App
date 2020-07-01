from client import Client
import time

c1 = Client("Tim")
c2 = Client("Joe")

c1.send_message("hello")
time.sleep(1)
c2.send_message("hello")
time.sleep(1)
c1.send_message("What's up?")
time.sleep(1)
c2.send_message("Nothing much")
time.sleep(5)
c1.disconnect()
time.sleep(1)
c2.disconnect()









# from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
# import time
#
# # GLOBAL CONSTANTS
# HOST = "localhost"
# PORT = 5500
# ADDR = (HOST, PORT)
# BUFSIZ = 512
#
# # GLOBAL VARIABLES
# messages = []
#
# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(ADDR)
#
#
# def receive_messages():
#     while True:
#         try:
#             msg = client_socket.recv(BUFSIZ).decode()
#             messages.append(msg)
#             print(msg)
#         except Exception as e:
#             print("[EXCEPTION]", e)
#             break
#
#
# def send_message(msg):
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#
#
# receive_thread = Thread(target=receive_messages)
# receive_thread.start()
#
# send_message("Tim")
# time.sleep(10)
# send_message("hello")
# time.sleep(2)
# send_message("{quit}")