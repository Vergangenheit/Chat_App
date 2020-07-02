from client import Client
import time
from threading import Thread

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


def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10th of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages
        for msg in new_messages:  # display new messages
            print(msg)
            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()
