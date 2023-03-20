import tkinter as tk
from tkinter import ttk, scrolledtext
from controller import *

# contains a dropdown of users to message (default is group)
# contains an input box for your message to send
# contains a button to send the message
class MessageBar(tk.Frame):
    pass


# displays a list of all users currently online that aren't you
class ActiveUsers(tk.Frame):
    pass


# displays the title, your username, and a logout button
class TitleBar(tk.Frame):
    pass


# displays all the messages in chat
class MessageList(tk.Frame):
    pass

# displays the other items in this file
class ChatPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        
        # Constants
        self.ENTER_TEXT_HERE = "Enter text here..."

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   STYLING   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        style = ttk.Style()
        style.configure('Custom.TEntry', padding=10, height=10, width=50)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        # Create label for the online users listbox
        self.online_users_label = ttk.Label(self, text="Online users", font=('Arial', '10', 'bold'))

        # Create listbox for online users using dummy data for now
        self.online_users_listbox = tk.Listbox(self, height=20)
        users = ['User 1', 'User 2', 'User 3', 'User 4']
        for user in users:
            self.online_users_listbox.insert(tk.END, user)
        
        # Create dropdown menu for selecting a user
        self.user_var = tk.StringVar(self)
        self.user_dropdown = ttk.Combobox(self, textvariable=self.user_var, values=users)
        self.user_dropdown.current(0)

        # Create Chat Room label
        self.chat_room_label = ttk.Label(self, text="Chat Room", font=('Arial', '10', 'bold'))

        # Create send button
        self.send_button = ttk.Button(self, text="Send", command=self.send_message)

        # Create scrolledtext widget
        self.scrolled_text_chatbox = scrolledtext.ScrolledText(self, wrap='word')

        # Create input area
        self.entry = ttk.Entry(self, style='Custom.TEntry')
        self.entry.insert(0, self.ENTER_TEXT_HERE)

        # Create logout button 
        # ## MISSING EVENT HANDLER FOR LOGGING OUT
        self.logout_button = ttk.Button(self, text="Log Out") 

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.online_users_label.grid(row=0, column=2, sticky="w", padx=10, pady=2)

        self.online_users_listbox.grid(row=1, column=2, sticky="nsew", padx=10)

        self.chat_room_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.scrolled_text_chatbox.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10)
        self.scrolled_text_chatbox.config(state='disabled')

        self.user_dropdown.grid(row=2, column=2, sticky="sew", padx=10, pady=5)

        self.entry.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.send_button.grid(row=2, column=2, sticky="nwe", padx=10, pady=5)

        self.logout_button.place(relx=0.77, rely=0, anchor="ne")

        # Configure grid weights
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Disable the list box
        self.online_users_listbox.config(state='disabled')

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.entry.bind("<Return>", self.send_message) # binds hitting the enter key to the send_message() event handler
        self.entry.bind("<FocusIn>", self.on_entry_click) # gets rid of the "Enter text here..." when clicking into the Entry
        self.entry.bind("<FocusOut>", self.on_focusout) # brings back the "Enter text here..." when clicking off of the Entry
        self.user_dropdown.bind('<<ComboboxSelected>>', self.select_user) # calls a method that print the user that is selected (no real functionality atm)

    # Event handler to select a User from the Combobox
    def select_user(self, event):
        print(self.user_dropdown.get())

    # Event handler for <FocusIn> event
    def on_entry_click(self, event):
        if self.entry.get() == self.ENTER_TEXT_HERE:
            self.entry.delete(0, "end") # remove all the text in the entry

    # Event handler for <FocusOut> event
    def on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.ENTER_TEXT_HERE)

    # Event handler for sending a message
    def send_message(self, event=None):
        # Get message from input area
        message = self.entry.get()

        # Prevents "Enter text here..." being sent to the chat room
        if message == self.ENTER_TEXT_HERE:
            return
        send_message(message, )
        # if message:
        #     # Enable the chatbox to insert the message
        #     self.scrolled_text_chatbox.config(state='normal')
        #     # Add message to chatbox
        #     self.scrolled_text_chatbox.insert(tk.END, f"{message}\n")
        #     # Disable the chat box
        #     self.scrolled_text_chatbox.config(state='disable')
        #     self.entry.delete('0', 'end')
        return "break" # prevents the default behavior of the "Return"
    
    def update_user_list(self, users):
        self.online_users_listbox.delete(0, tk.END)
        for user in users:
            self.online_users_listbox.insert(tk.END, user)
    
    def update_message_list(self, messages):
        self.scrolled_text_chatbox.config(state='normal')
        self.scrolled_text_chatbox.delete('1.0', tk.END)
        for message in messages:
            self.scrolled_text_chatbox.insert(tk.END, message + '\n')
        self.scrolled_text_chatbox.config(state='disabled')