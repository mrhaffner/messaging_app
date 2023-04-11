import tkinter as tk
from tkinter import ttk


# displays the login form
class CreateAccountPopup(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.view = parent
        # constants
        self.USERNAME_TEXT = "Username"
        self.PASSWORD_TEXT = "Password"

        # set focus on the this window, which means it will capture events such as key presses including escape key events
        self.focus_set()

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   STYLING   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label = tk.Label(self, text="Create An Account", font=('Times', '20'))

        self.usernameEntry = ttk.Entry(self)
        self.usernameEntry.insert(0, self.USERNAME_TEXT)

        self.passwordEntry = ttk.Entry(self, show="*")
        self.passwordEntry.insert(0, self.PASSWORD_TEXT)

        self.createAccountBtn = tk.Button(self, text="Create Account", command=self._create_account)
        self.backBtn = tk.Button(self, text="Back", command=self._back_to_login)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label.pack(pady=50,padx=0)
        self.usernameEntry.pack(pady=10, padx=0)
        self.passwordEntry.pack(pady=10, padx=0)
        self.createAccountBtn.pack(side="right", anchor="n", pady=15, padx=(10, 285))
        self.backBtn.pack(side="left", anchor="n", pady=15, padx=(290, 10))

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        #self.entry.bind("<Return>", self.send_message) # binds hitting the enter key to the send_message() event handler
        self.usernameEntry.bind("<FocusIn>", self._on_username_entry_click)
        self.passwordEntry.bind("<FocusIn>", self._on_pw_entry_click) 
        self.usernameEntry.bind("<FocusOut>", self._on_focusout) 
        self.passwordEntry.bind("<FocusOut>", self._on_focusout)
        self.passwordEntry.bind("<Return>", self._create_account)
        self.bind("<Escape>", self.escape_key_pressed)

    def _back_to_login(self):
        self.view.show_login_page()

    def escape_key_pressed(self, event):
        self._back_to_login()
    
    def _create_account(self, event):
        user_name = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if (user_name != self.USERNAME_TEXT and password != self.PASSWORD_TEXT):
            self.view.send_new_account(user_name, password)

    # gets rid of the "Enter text here..." when clicking into the Entry
    def _on_username_entry_click(self, event):
        if self.usernameEntry.get() == self.USERNAME_TEXT:
            self.usernameEntry.delete(0, "end")

    # gets rid of the "Enter text here..." when clicking into the Entry
    def _on_pw_entry_click(self, event):
        if self.passwordEntry.get() == self.PASSWORD_TEXT:
            self.passwordEntry.delete(0, "end")

    # brings back the "Enter text here..." when clicking off of the Entry
    def _on_focusout(self, event):
        if self.usernameEntry.get() == "":
            self.usernameEntry.insert(0, self.USERNAME_TEXT)
        
        if self.passwordEntry.get() == "":
            self.passwordEntry.insert(0, self.PASSWORD_TEXT)