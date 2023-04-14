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
from component.main_window import ChatPage
from component.login_popup import LoginPopup
from component.create_account_popup import CreateAccountPopup
from model.user import CurrentUser, User, UserList
from model.message import MessageList
import controller


class ChatView(tk.Tk):

    def __init__(self):
        super().__init__()

        self.current_user = CurrentUser()
        self.message_list = MessageList()
        self.user_list = UserList()
        
        self.user_list.subscribe(self) 
        self.current_user.subscribe(self)
        self.message_list.subscribe(self)

        self.title("Messaging Application")
        self.geometry("720x550")
        self.resizable(True, True)

        # parent will be the top-level widget in the application, which can hold and manage other widgets.
        parent = tk.Frame(self)
        parent.pack(side="top", fill="both", expand=True)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # initialize dictionary to hold frames
        self.frames = {}

        # Assign ChatPage and LogInPage classes to instance variables
        self.chat_page = ChatPage
        self.log_in_page = LoginPopup
        self.create_account_page = CreateAccountPopup
        self.pages = (self.chat_page, self.log_in_page, self.create_account_page)
        # Loop through the frames and create instances of each
        for TtkFrame in self.pages:
            frame = TtkFrame(self, parent) 
            self.frames[TtkFrame] = frame
            # place each frame in the parent grid
            frame.grid(row=0, column=0, sticky="nsew")

        # initially show the login page
        self.show_frame(self.log_in_page)

    def show_frame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()
    
    def send_message(self, message, username):
        if username == "":
            return
        elif username == "group":
            user = User("group")
        else:
            user = self.user_list.get_by_name(username)  # returns user or None

        controller.send_message(message, user)
        
    def show_login(self):
        """Switches to login page when no observable needs to be updated"""
        self.show_frame(self.log_in_page)

    def show_create_account(self):
        """Switches to account creation page when no observable needs to be updated"""
        self.show_frame(self.create_account_page)

    def send_new_account(self, user_name, password):
        """
        Sends a new account to the controller to be sent to server
        and returns the response
        """
        return controller.create_account(user_name, password)
            
    def log_out(self):
        controller.logout()
    
    def log_in(self, user_name, password):
        return controller.login(user_name, password)

    def get_user_list(self):
        return self.user_list.get_all()

    # takes in an object and updates the view
    def publish(self, publisher):
        chat_page = self.frames[self.chat_page]
        if isinstance(publisher, UserList):
            # Update user list in chat page
            chat_page._update_user_listbox(publisher.get_all())
            chat_page._update_user_dropdown_combobox(publisher.get_all())
        elif isinstance(publisher, CurrentUser):
            ''' what this is doing in response to the CurrentUser changing
            is either going to the log in screen or the main window '''
            # check if there is a current user and if so, then switch the screen to chat page.
            if publisher.exists():
                self.user_list.current_user = self.current_user._user
                chat_page._update_current_user_label(self.current_user._user.name)
                self.show_frame(self.chat_page)
            # else show the login page
            else: 
                self.user_list.current_user = None
                self.show_frame(self.log_in_page)
        elif isinstance(publisher, MessageList):
            # Update message list in chat page
            chat_page._update_message_list_entries(publisher.get_all())
            