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
        self.users = []

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
        
        # users = ['User 1', 'User 2', 'User 3', 'User 4']
        # for user in users:
        #     self.online_users_listbox.insert(tk.END, user)

        # Create dropdown menu for selecting a user
        self.user_var = tk.StringVar(self)
        self.user_dropdown_combobox = ttk.Combobox(self, textvariable=self.user_var, values=self.users)
        # I think we're gonna want to set the state to readonly right off the bat
        # I'm not sure if we'll be able to select a user if its readonly just yet, so this may need to be changed to 'normal' here.
        self.user_dropdown_combobox['state'] = 'readonly' 
        # self.user_dropdown.current(0)

        # Create Chat Room label
        self.chat_room_label = ttk.Label(self, text="Chat Room", font=('Arial', '10', 'bold'))

        # Create send button
        self.send_button = ttk.Button(self, text="Send", command=self._send_message)

        # Create scrolledtext widget
        self.scrolled_text_chatbox = scrolledtext.ScrolledText(self, wrap='word')

        # Create input area
        self.entry = ttk.Entry(self, style='Custom.TEntry')
        self.entry.insert(0, self.ENTER_TEXT_HERE)

        # Create logout button 
        self.logout_button = ttk.Button(self, text="Log Out", command=self._logout) 

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.online_users_label.grid(row=0, column=2, sticky="w", padx=10, pady=2)

        self.online_users_listbox.grid(row=1, column=2, sticky="nsew", padx=10)

        self.chat_room_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.scrolled_text_chatbox.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10)
        self.scrolled_text_chatbox.config(state='disabled')

        self.user_dropdown_combobox.grid(row=2, column=2, sticky="sew", padx=10, pady=5)

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
        self.entry.bind("<Return>", self._send_message) # binds hitting the enter key to the send_message() event handler
        self.entry.bind("<FocusIn>", self._on_entry_click) # gets rid of the "Enter text here..." when clicking into the Entry
        self.entry.bind("<FocusOut>", self._on_focusout) # brings back the "Enter text here..." when clicking off of the Entry
        self.user_dropdown_combobox.bind('<<ComboboxSelected>>', self._select_user) # calls a method that print the user that is selected (no real functionality atm)

    # Event handler to select a User from the Combobox
    def _select_user(self, event):
        return self.user_dropdown_combobox.get()

    # Event handler for <FocusIn> event
    def _on_entry_click(self, event):
        if self.entry.get() == self.ENTER_TEXT_HERE:
            self.entry.delete(0, "end") # remove all the text in the entry

    # Event handler for <FocusOut> event
    def _on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.ENTER_TEXT_HERE)

    # TODO: Implement logic so that the chatbox can be disabled after sending a message
    # Event handler for sending a message
    def _send_message(self, event=None):
        # Get message from input area
        message = self.entry.get()

        # Prevents "Enter text here..." being sent to the chat room
        if message == self.ENTER_TEXT_HERE:
            return
        
        # Gets the username of the user that is selected from the user drop down menu
        user_name = self.user_dropdown_combobox.get()
        # Searches for the user in self.users
        for user in self.users:
            # if the user is found, send_message() from the controller is called.
            if user_name == str(user):
                send_message(message, user)
        # if message:
        #     # Enable the chatbox to insert the message
        #     self.scrolled_text_chatbox.config(state='normal')
        #     # Add message to chatbox
        #     self.scrolled_text_chatbox.insert(tk.END, f"{message}\n")
        #     # Disable the chat box
        #     self.scrolled_text_chatbox.config(state='disable')
        #     self.entry.delete('0', 'end')
        return "break" # prevents the default behavior of the "Return"
    
    # Calls the controller logout() method to log the user out.
    def _logout(self):
        logout()
    
    # Updates the list box that contains the online users, not the drop down menu.
    def _update_user_listbox(self, users):
        self.online_users_listbox.delete(0, tk.END)
        for user in users:
            self.online_users_listbox.insert(tk.END, user)
            if user not in self.users:
                self.users.append(user)
    
    # Updates the drop down menu of users that the user can select to send messages to. 
    def _update_user_dropdown_combobox(self, users):
        self.user_dropdown_combobox['state'] = 'normal'
        self.user_dropdown_combobox.configure(values=users)
        self.user_dropdown_combobox['state'] = 'readonly'
    
    # Updates the list of message entries in the chat room. 
    def _update_message_list_entries(self, messages):
        self.scrolled_text_chatbox.config(state='normal')
        self.scrolled_text_chatbox.delete('1.0', tk.END)
        for message in messages:
            self.scrolled_text_chatbox.insert(tk.END, message + '\n')
        self.scrolled_text_chatbox.config(state='disabled')