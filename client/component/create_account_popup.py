import tkinter as tk
from tkinter import ttk, messagebox


class CreateAccountPopup(ttk.Frame):
    """Defines functionality of the create account page"""

    def __init__(self, parent, container):
        """Initialize this PopUp"""
        super().__init__(container)

        self.view = parent
        self.USERNAME_TEXT = "Username"
        self.PASSWORD_TEXT = "Password"

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label = tk.Label(self, text="Create Account Page", font=("Times", "20"))

        self.usernameEntry = ttk.Entry(self)
        self.usernameEntry.insert(0, self.USERNAME_TEXT)

        self.passwordEntry = ttk.Entry(self, show="*")
        self.passwordEntry.insert(0, self.PASSWORD_TEXT)

        self.createAccountBtn = tk.Button(self, text="Create Account", command=self._create_account)
        self.backToLoginBtn = tk.Button(self, text="Back to Login", command=self._show_login)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label.pack(pady=50,padx=0)
        self.usernameEntry.pack(pady=10, padx=0)
        self.passwordEntry.pack(pady=10, padx=0)
        self.createAccountBtn.pack(pady=10, padx=0)
        self.backToLoginBtn.pack(pady=10, padx=0)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.usernameEntry.bind("<FocusIn>", self._on_username_entry_click)
        self.passwordEntry.bind("<FocusIn>", self._on_pw_entry_click) 
        self.usernameEntry.bind("<FocusOut>", self._on_focusout) 
        self.passwordEntry.bind("<FocusOut>", self._on_focusout) 
    
    def _create_account(self):
        """
        When the create account button is pushed, get the username and password
        from the text fields, and send the information through the view, controller,
        then server. Based on the response, can either log in or show an error
        message.
        """
        user_name = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if (user_name != self.USERNAME_TEXT and password != self.PASSWORD_TEXT):
            create_account_response = self.view.send_new_account(user_name, password)

            if create_account_response == 401:
                messagebox.showerror("Invalid Credentials", "Invalid Username/Password")
            elif create_account_response == 503:
                messagebox.showerror("Connection refused", "Server is down")
            elif create_account_response != 200:
                messagebox.showerror("Failed to create account", "Error code: " + str(create_account_response))
            else:
                self._show_login()
    
    def _show_login(self):
        """When the back to login button is pushed, reset the fields and show the page"""
        self._reset_fields()
        self.view.show_login()

    def _on_username_entry_click(self, event):
        """Clear text in username field if it is the initial text"""
        if self.usernameEntry.get() == self.USERNAME_TEXT:
            self.usernameEntry.delete(0, "end")

    def _on_pw_entry_click(self, event):
        """Clear text in password field if it is the initial text"""
        if self.passwordEntry.get() == self.PASSWORD_TEXT:
            self.passwordEntry.delete(0, "end")

    def _on_focusout(self, event):
        """Brings back initial text if user clicks out after nothing is entered"""
        if self.usernameEntry.get() == "":
            self.usernameEntry.insert(0, self.USERNAME_TEXT)
        
        if self.passwordEntry.get() == "":
            self.passwordEntry.insert(0, self.PASSWORD_TEXT)

    def _reset_fields(self):
        """Helper function to clear everything in fields and reset them"""
        self.usernameEntry.delete(0, tk.END)
        self.usernameEntry.insert(0, self.USERNAME_TEXT)
        self.passwordEntry.delete(0, tk.END)
        self.passwordEntry.insert(0, self.PASSWORD_TEXT)