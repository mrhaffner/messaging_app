import controller
import tkinter as tk

from component.main_window import ChatPage
from component.login_popup import LoginPopup
from component.create_account_popup import CreateAccountPopup
from model.user import CurrentUser, User, UserList
from model.message import MessageList


class ChatView(tk.Tk):
    """
    ChatView is a tkinter-based user interface for the messaging application.
    It manages the display and interactions for chat, login and account creation components.
    ChatView also subscribes to changes in the model classes and updates the UI accordingly.
    """

    def __init__(self):
        """
        Initializes the ChatView class, which is the main application window for the messaging 
        application. Sets up the frames, subscribes to the models, configures the window
        properties, and initializes the UI components.
        """
        super().__init__()

        self.current_user = CurrentUser()  # Instantiates CurrentUser singleton
        self.message_list = MessageList()  # Instantiates MessageList singleton
        self.user_list = UserList()  # Instantiates UserList singleton
        
        # Subscribe ChatView to UserList's updates for displaying changes in the list of users
        self.user_list.subscribe(self)
        # Subscribe ChatView to CurrentUser's updates for displaying changes in the current user's state
        self.current_user.subscribe(self)
        # Subscribe ChatView to MessageList's updates for displaying changes in the list of messages
        self.message_list.subscribe(self)

        # Set the title of the application window
        self.title("Messaging Application")
        # Set the default size of the application window
        self.geometry("720x550")
        # Allow the application window to be resizable in both width and height
        self.resizable(True, True)
        # Bind the closing of the application window to the _on_close method
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # top-level widget in the application, which can hold and manage other widgets.
        parent = tk.Frame(self)
        parent.pack(side="top", fill="both", expand=True)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Initialize dictionary to hold frames
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

    def _on_close(self):
        """
        Handles the event when the user clicks the exit button on the top right corner of the 
        window. Logs the user out and destroys the application.
        """
        self.log_out()
        self.destroy()


    def show_frame(self, frame):
        """
        Raises the given frame to the top of the window, making it visible.

        Args:
            frame (class): The frame class to be shown.
        """
        frame = self.frames[frame]
        frame.tkraise()

    def send_message(self, message, username):
        """
        Sends a message to the specified user or group.
        """
        if username == "":
            return
        elif username == "group":
            user = User("group")
        else:
            user = self.user_list.get_by_name(username)  # returns user or None

        controller.send_message(message, user)

    def show_login(self):
        """Shows the login frame."""
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
        """Logs the current user out."""
        controller.logout()

    def log_in(self, user_name, password):
        """
        Sends a request to the controller to log in with the given username and password.
        """
        return controller.login(user_name, password)

    def kick_user(self, user_name):
        """
        Sends a request to kick a user with the given username.
        """
        controller.kick(user_name)

    def get_user_list(self):
        """
        Retrieves the list of all users.
        """
        return self.user_list.get_all()

    def publish(self, publisher):
        """Updates the view based on the changes in the publisher's state."""
        chat_page = self.frames[self.chat_page]
        if isinstance(publisher, UserList):
            # Update user list in chat page
            chat_page._update_user_listbox(publisher.get_all())
            chat_page._update_user_dropdown_combobox(publisher.get_all())
        elif isinstance(publisher, CurrentUser):
            # Check if there is a current user and if so, then switch the screen to chat page.
            if publisher.exists():
                self.user_list.current_user = self.current_user._user
                chat_page._update_current_user_label(self.current_user._user.name)

                if self.current_user._user.name.lower() == 'admin':
                    chat_page.show_kick_button()

                self.show_frame(self.chat_page)
            else: # else show the login page
                self.user_list.current_user = None
                self.show_frame(self.log_in_page)
        elif isinstance(publisher, MessageList):
            # Update message list in chat page 
            chat_page._update_message_list_entries(publisher.get_all()) 