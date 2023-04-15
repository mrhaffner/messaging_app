import tkinter as tk

from tkinter import ttk, scrolledtext


class ChatPage(ttk.Frame):
    """
    ChatPage class represents the main chat window, where users can interact with each other.
    It inherits from the tkinter.ttk.Frame class and provides a layout for chat messages, online
    users, and message input area along with related functionality.
    """

    def __init__(self, parent, container):
        """
        Initializes the ChatPage frame with its parent and container, and sets up the layout, 
        widgets, and event bindings.
        """
        super().__init__(container)
        self.parent = parent

        # Constants
        self.ENTER_TEXT_HERE = "Enter text here..."

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   STYLING   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        style = ttk.Style()
        style.configure("Custom.TEntry", padding=10, height=10, width=50)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        # Create label for the online users listbox
        self.online_users_label = ttk.Label(self, text="Online users", font=("Arial", "10", "bold"))

        # Create listbox for online users using dummy data for now
        self.online_users_listbox = tk.Listbox(self, selectmode="single", height=20)

        # Create dropdown menu for selecting a user
        self.user_var = tk.StringVar(self)
        self.user_dropdown_combobox = ttk.Combobox(self, textvariable=self.user_var, values=parent.get_user_list)

        # Set the user dropdown combobox state to 'readonly' to prevent users from typing in the input area of the combobox
        self.user_dropdown_combobox["state"] = "readonly" 

        # Create Chat Room label
        self.chat_room_label = ttk.Label(self, text="Chat Room", font=("Arial", "10", "bold"))

        # Create send button
        self.send_button = ttk.Button(self, text="Send", command=self._send_message)

        # Create scrolledtext widget
        self.chatbox_scrolled_text = scrolledtext.ScrolledText(self, wrap="word")
        self.chatbox_scrolled_text.tag_config("DM", foreground="blue")

        # Create input area
        self.entry = ttk.Entry(self, style="Custom.TEntry")
        self.entry.insert(0, self.ENTER_TEXT_HERE)

        # Create logout button 
        self.logout_button = ttk.Button(self, text="Log out", command=self._logout) 

        # Creates the current user label, i.e., @admin
        self.current_user_label = ttk.Label(self, text="@", font=("Arial", "10", "bold"))

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
        # self.kick_button will be added to the grid based on the condition that the current user is an admin via show_kick_button method

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

        # Disable chat box
        self.chatbox_scrolled_text.config(state="disabled")

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.entry.bind("<Return>", self._send_message)
        self.entry.bind("<FocusIn>", self._on_entry_click)
        self.entry.bind("<FocusOut>", self._on_focusout)

    def _on_entry_click(self, event):
        """Event handler for when the user clicks on the input area."""
        if self.entry.get() == self.ENTER_TEXT_HERE:
            self.entry.delete(0, "end")  # remove all the text in the entry

    def _on_focusout(self, event):
        """Event handler for when the user clicks outside of the input area."""
        if self.entry.get() == "":
            self.entry.insert(0, self.ENTER_TEXT_HERE)

    def _send_message(self, event=None):
        """Send a message in the chat, handling private messages if a user is selected."""
        message = self.entry.get()  # Get message from input area

        # Prevents "Enter text here..." being sent to the chat room
        if message == self.ENTER_TEXT_HERE:
            return
        
        # Gets the username of the user that is selected from the user drop down menu
        user_name = self.user_dropdown_combobox.get()

        if message:
            self.parent.send_message(message, user_name)

        return "break"  # prevents the default behavior of the "Return"

    def _logout(self):
        """Log out the user and return to the login page."""
        self.parent.log_out()

    def _kick_user(self, user_name):
        """Kick a user from the chat room."""
        self.parent.kick_user(user_name)  # Calls kick_user method on View

    def _select_user_to_kick(self):
        """Select a user to be kicked from the chat room."""
        selected_users = self.online_users_listbox.curselection()

        if len(selected_users) == 1:  # Makes sure something is selected
            index_of_user_to_kick = selected_users[0]
            selected_user = self.online_users_listbox.get(index_of_user_to_kick)

            self._kick_user(selected_user)

    def show_kick_button(self):
        """Show the kick button if the current user is the admin."""
        self.kick_button.grid(row=0, column=4, sticky="e", padx=10, pady=2)
        self.online_users_listbox.config(state="normal") # Enables the list box for the admin

    def _update_user_listbox(self, users):
        """Update the list of online users displayed in the listbox."""
        self.online_users_listbox.config(state="normal")
        self.online_users_listbox.delete(0, tk.END)
        for user in users:
            self.online_users_listbox.insert(tk.END, user.name)
        if self.parent.current_user._user is not None and self.parent.current_user._user.name != "admin":
            self.online_users_listbox.config(state="disabled")

    def _update_user_dropdown_combobox(self, users):
        """Update the user dropdown menu with the current list of online users."""
        self.user_dropdown_combobox["state"] = "normal"
        self.user_dropdown_combobox.configure(values=["group"] + [user.name for user in users])
        self.user_dropdown_combobox["state"] = "readonly"

    def _update_message_list_entries(self, messages):
        """Update the list of message entries displayed in the chat room."""
        self.chatbox_scrolled_text.config(state="normal")
        self.chatbox_scrolled_text.delete("1.0", tk.END)
        for message in messages:
            text = f"[{message.sender.name}] {message.text}\n"
            if message.type == "DM":
                self.chatbox_scrolled_text.insert(tk.END, text, "DM")
            else:
                self.chatbox_scrolled_text.insert(tk.END, text)
        self.chatbox_scrolled_text.config(state="disabled")

    def _update_current_user_label(self, username):
        """Update the current user label with the username."""
        self.current_user_label.config(text="@" + username)