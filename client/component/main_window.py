import tkinter as tk
from tkinter import ttk, scrolledtext
import typing



# displays the other items in this file
class ChatPage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent

        # Constants
        self.ENTER_TEXT_HERE = "Enter text here..."

        # set focus on the this window, which means it will capture events such as key presses including escape key events
        self.focus_set()

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
        self.online_users_listbox = tk.Listbox(self, selectmode="single", height=20)

        # Create dropdown menu for selecting a user
        self.user_var = tk.StringVar(self)
        self.user_dropdown_combobox = ttk.Combobox(self, textvariable=self.user_var, values=parent.get_user_list)
        # I think we're gonna want to set the state to readonly right off the bat
        # I'm not sure if we'll be able to select a user if its readonly just yet, so this may need to be changed to 'normal' here.
        self.user_dropdown_combobox['state'] = 'readonly' 

        # Create Chat Room label
        self.chat_room_label = ttk.Label(self, text="Chat Room", font=('Arial', '10', 'bold'))

        # Create send button
        self.send_button = ttk.Button(self, text="Send", command=self._send_message)

        # Create scrolledtext widget
        self.chatbox_scrolled_text = scrolledtext.ScrolledText(self, wrap='word')
        self.chatbox_scrolled_text.tag_config('DM', foreground='blue')

        # Create input area
        self.entry = ttk.Entry(self, style='Custom.TEntry')
        self.entry.insert(0, self.ENTER_TEXT_HERE)

        # Create logout button 
        self.logout_button = ttk.Button(self, text="Log out", command=self._logout) 

        # Creates the current user label, i.e., @admin
        self.current_user_label = ttk.Label(self, text="@", font=('Arial', '10', 'bold'))

        # Creates the kick button that the admin uses to kick users
        self.kick_button = ttk.Button(self, text="Kick", command=self._select_user_to_kick) 

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~  There are 3 three rows and 4 columns within the chat page.  ~~~~~~~~~~~###

        # ROW 0
        self.chat_room_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.current_user_label.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        self.logout_button.grid(row=0, column=2, sticky="e", padx=10, pady=2)
        self.online_users_label.grid(row=0, column=3, sticky="w", padx=10, pady=2)
        # Kick Button will be added to the grid based on the condition that the current user is an admin (show_kick_button method)

        # ROW 1
        self.chatbox_scrolled_text.grid(row=1, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=10)
        self.online_users_listbox.grid(row=1, column=3, columnspan=2, sticky="nsew", padx=10)

        # ROW 2
        self.entry.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.send_button.grid(row=2, column=3, columnspan=2, sticky="nwe", padx=10, pady=5)
        self.user_dropdown_combobox.grid(row=2, column=3, columnspan=2, sticky="sew", padx=10, pady=5)

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
        # self.user_dropdown_combobox.bind('<<ComboboxSelected>>', self._select_user) # calls a method that print the user that is selected (no real functionality atm)
        # TODO: Should we log the user out if they hit escape within the ChatPage? 

    # Event handler for <FocusIn> event
    def _on_entry_click(self, event):
        if self.entry.get() == self.ENTER_TEXT_HERE:
            self.entry.delete(0, "end") # remove all the text in the entry

    # Event handler for <FocusOut> event
    def _on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.ENTER_TEXT_HERE)

    # TODO: Error handling
    # Event handler for sending a message
    def _send_message(self, event=None):
        # Get message from input area
        message = self.entry.get()

        # Prevents "Enter text here..." being sent to the chat room
        if message == self.ENTER_TEXT_HERE:
            return
        
        # Gets the username of the user that is selected from the user drop down menu
        user_name = self.user_dropdown_combobox.get()

        if message:
            self.parent.send_message(message, user_name)

        return "break" # prevents the default behavior of the "Return"
    
    # TODO: Provide other means for the user to log out besides hitting the log out button
    def _logout(self):
        self.parent.log_out()

    def _kick_user(self, user_name, index):
    # def _kick_user(self, user_name):
        self.parent.kick_user(user_name) # Calls kick_user method on View
        self.online_users_listbox.delete(index)
    
    def _select_user_to_kick(self):
        selected_users = self.online_users_listbox.curselection() # returns tuple with length of 1 or 0

        print(f'selected_indices: {selected_users}. length={len(selected_users)}')

        if len(selected_users) == 1: # Makes sure something is selected
            index_of_user_to_kick = selected_users[0]
            selected_user: str = self.online_users_listbox.get(index_of_user_to_kick)

            print(f'type: {type(selected_user)} selected_username: {selected_user}')

            self._kick_user(selected_user, index_of_user_to_kick)
            self._remove_user_from_combobox(selected_user)
    
    # Private method that deletes removes the user from the comboxbox after the admin kicks a user
    def _remove_user_from_combobox(self, user_name):
        if user_name != "group":
            index = self.user_dropdown_combobox["values"].index(user_name)
            self.user_dropdown_combobox.delete(index)

    # Shows the kick button if the CurrentUser is the Admin
    def show_kick_button(self):
        self.kick_button.grid(row=0, column=4, sticky="e", padx=10, pady=2)
        self.online_users_listbox.config(state='normal') # Enables the list box for the admin
    
    # Updates the list box that contains the online users, not the drop down menu.
    def _update_user_listbox(self, users):
        self.online_users_listbox.config(state='normal')
        self.online_users_listbox.delete(0, tk.END)
        for user in users:
            self.online_users_listbox.insert(tk.END, user.name)
        self.online_users_listbox.config(state='disabled')

    # Updates the list box that contains the online users, not the drop down menu.
    def _update_user_listbox_unrestricted(self, users):
        self.online_users_listbox.config(state='normal')
        self.online_users_listbox.delete(0, tk.END)
        for user in users:
            self.online_users_listbox.insert(tk.END, user.name)
    
    # Updates the drop down menu of users that the user can select to send messages to. 
    def _update_user_dropdown_combobox(self, users):
        self.user_dropdown_combobox['state'] = 'normal'
        self.user_dropdown_combobox.configure(values=["group"] + [user.name for user in users])
        self.user_dropdown_combobox['state'] = 'readonly'
    
    # Updates the list of message entries in the chat room. 
    def _update_message_list_entries(self, messages):
        self.chatbox_scrolled_text.config(state='normal')
        self.chatbox_scrolled_text.delete('1.0', tk.END)
        for message in messages:
            text = f"[{message.sender.name}] {message.text}\n"
            if message.type == "DM":
                self.chatbox_scrolled_text.insert(tk.END, text, "DM")
            else:
                self.chatbox_scrolled_text.insert(tk.END, text)
        self.chatbox_scrolled_text.config(state='disabled')

    # Updates current user label
    def _update_current_user_label(self, username):
        self.current_user_label.config(text="@" + username)