# subscribes to changes in the model ie pub/sub aka observer pattern
# contains state about what is currently being displayed on the screen
# ie if you are connected/disconnected
# contains the model instances:
#   UserList singleton
#   MessageList singleton
#   current User (should indicate if there is none aka not logged in)
# displays the components
# buttons in the components generally call methods in the controller

import tkinter as tk


class ChatView(tk.Tk):

    def __init__(self):
        super().__init__()

        # settings
        self.title("Messaging App")
        self.geometry("500x500")
        self.resizable(False, False)