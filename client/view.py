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
from model.user import CurrentUser, UserList
from model.message import MessageList

class ChatView(tk.Tk):

    def __init__(self):
        super().__init__()

        self.user_list = UserList()
        self.current_user = CurrentUser()
        self.message_list = MessageList()

        self.user_list.subscribe('''pass in something''') 
        self.current_user.subscribe('''pass in something''')
        self.message_list.subscribe('''pass in something''')

        self.title("Messaging Application")
        self.geometry("720x550")
        self.resizable(True, True)

        # parent will be the top-level widget in the application, which can hold and manage other widgets.
        parent = tk.Frame(self)
        parent.pack(side="top", fill="both", expand=True)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.ChatPage = ChatPage
        self.LogInPage = LoginPopup

        for F in (ChatPage, LoginPopup):
            frame = F(self, parent)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPopup)
    
    # takes in an object and updates the view
    def publish(self):
        pass

    def show_frame(self, frame):
        frame = self.frames[frame]
        # menubar = frame.create_menubar(self)
        # self.configure(menu=menubar)
        frame.tkraise()

# class ChatPage(ttk.Frame):
#     def __init__(self, parent, container):
#         super().__init__(container)
#         self.parent = parent
        
#         # Constants
#         self.ENTER_TEXT_HERE = "Enter text here..."

#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   STYLING   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         style = ttk.Style()
#         style.configure('Custom.TEntry', padding=10, height=10, width=50)


#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         # Create label for the online users listbox
#         self.online_users_label = ttk.Label(self, text="Online users", font=('Arial', '10', 'bold'))

#         # Create listbox for online users using dummy data for now
#         self.online_users_listbox = tk.Listbox(self, height=20)
#         users = ['User 1', 'User 2', 'User 3', 'User 4']
#         for user in users:
#             self.online_users_listbox.insert(tk.END, user)
        
#         # Create dropdown menu for selecting a user
#         self.user_var = tk.StringVar(self)
#         self.user_dropdown = ttk.Combobox(self, textvariable=self.user_var, values=users)
#         self.user_dropdown.current(0)

#         # Create Chat Room label
#         self.chat_room_label = ttk.Label(self, text="Chat Room", font=('Arial', '10', 'bold'))

#         # Create send button
#         self.send_button = ttk.Button(self, text="Send", command=self.send_message)

#         # Create scrolledtext widget
#         self.scrolled_text_chatbox = scrolledtext.ScrolledText(self, wrap='word')

#         # Create input area
#         self.entry = ttk.Entry(self, style='Custom.TEntry')
#         self.entry.insert(0, self.ENTER_TEXT_HERE)

#         # Create logout button 
#         # ## MISSING EVENT HANDLER FOR LOGGING OUT
#         self.logout_button = ttk.Button(self, text="Log Out") 


#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         self.online_users_label.grid(row=0, column=2, sticky="w", padx=10, pady=2)

#         self.online_users_listbox.grid(row=1, column=2, sticky="nsew", padx=10)

#         self.chat_room_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

#         self.scrolled_text_chatbox.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10)
#         self.scrolled_text_chatbox.config(state='disabled')

#         self.user_dropdown.grid(row=2, column=2, sticky="sew", padx=10, pady=5)

#         self.entry.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

#         self.send_button.grid(row=2, column=2, sticky="nwe", padx=10, pady=5)

#         self.logout_button.place(relx=0.77, rely=0, anchor="ne")

#         # Configure grid weights
#         self.columnconfigure(1, weight=1)
#         self.rowconfigure(1, weight=1)

#         # Disable the list box
#         self.online_users_listbox.config(state='disabled')


#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
#         self.entry.bind("<Return>", self.send_message) # binds hitting the enter key to the send_message() event handler
#         self.entry.bind("<FocusIn>", self.on_entry_click) # gets rid of the "Enter text here..." when clicking into the Entry
#         self.entry.bind("<FocusOut>", self.on_focusout) # brings back the "Enter text here..." when clicking off of the Entry
#         self.user_dropdown.bind('<<ComboboxSelected>>', self.select_user) # calls a method that print the user that is selected (no real functionality atm)



#     # Event handler to select a User from the Combobox
#     def select_user(self, event):
#         print(self.user_dropdown.get())

#     # Event handler for <FocusIn> event
#     def on_entry_click(self, event):
#         if self.entry.get() == self.ENTER_TEXT_HERE:
#             self.entry.delete(0, "end") # remove all the text in the entry

#     # Event handler for <FocusOut> event
#     def on_focusout(self, event):
#         if self.entry.get() == "":
#             self.entry.insert(0, self.ENTER_TEXT_HERE)

#     # Event handler for sending a message
#     def send_message(self, event=None):
#         # Get message from input area
#         message = self.entry.get()

#         # Prevents "Enter text here..." being sent to the chat room
#         if message == self.ENTER_TEXT_HERE:
#             return

#         if message:
#             # Enable the chatbox to insert the message
#             self.scrolled_text_chatbox.config(state='normal')
#             # Add message to chatbox
#             self.scrolled_text_chatbox.insert(tk.END, f"{message}\n")
#             # Disable the chat box
#             self.scrolled_text_chatbox.config(state='disable')
#             self.entry.delete('0', 'end')
#         return "break" # prevents the default behavior of the "Return"
    
#     def create_menubar(self, parent):
#         # Creates Menu widget
#         menubar = tk.Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

#         # creates settings menu
#         settings_menu = tk.Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
#         menubar.add_cascade(label="File", menu=settings_menu)
#         settings_menu.add_command(label="NextFrame", command=lambda: parent.show_frame(parent.LogInPage))
#         settings_menu.add_command(label="Home", command=lambda: parent.show_frame(parent.ChatPage))
#         settings_menu.add_command(label="Close", command=lambda: parent.show_frame(parent.ChatPage))
#         settings_menu.add_separator()
#         settings_menu.add_command(label="Exit", command=parent.quit)  

#         # creates proccessing menu
#         processing_menu = tk.Menu(menubar, tearoff=0)
#         menubar.add_cascade(label="ExampleMenu1", menu=processing_menu)
#         processing_menu.add_command(label="ExampleMenu2")
#         processing_menu.add_separator()

#         # creates help menu
#         help_menu = tk.Menu(menubar, tearoff=0)
#         menubar.add_cascade(label="Help", menu=help_menu)
#         help_menu.add_command(label="About", command=utils.about)
#         help_menu.add_separator()

#         return menubar

# class LogInPage(ttk.Frame):
#     def __init__(self, parent, container):
#         super().__init__(container)

#         label = tk.Label(self, text="Log In Page", font=('Times', '20'))
#         label.pack(pady=0,padx=0)

#         ## ADD CODE HERE TO DESIGN THIS PAGE

#     def create_menubar(self, parent):
#         menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

#         # creates a settings menu
#         settings_menu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
#         menubar.add_cascade(label="Settings", menu=settings_menu)
#         settings_menu.add_command(label="NextFrame", command=lambda: parent.show_frame(parent.LogInPage))
#         settings_menu.add_command(label="Home", command=lambda: parent.show_frame(parent.ChatPage))
#         settings_menu.add_command(label="Close", command=lambda: parent.show_frame(parent.ChatPage))
#         settings_menu.add_separator()
#         settings_menu.add_command(label="Exit", command=parent.quit)  

#         # BUG -----------------------------------------------------------------------------------------------------------
#         processing_menu = Menu(menubar, tearoff=0)
#         menubar.add_cascade(label="Validation", menu=processing_menu)
#         processing_menu.add_command(label="validate")
#         processing_menu.add_separator()

#         ## help menu
#         help_menu = Menu(menubar, tearoff=0)
#         menubar.add_cascade(label="Help", menu=help_menu)
#         help_menu.add_command(label="About", command=utils.about)
#         help_menu.add_separator()

#         return 