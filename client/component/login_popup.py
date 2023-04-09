import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# displays the login form
class LoginPopup(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        self.view = parent
        # constants
        self.USERNAME_TEXT = "Username"
        self.PASSWORD_TEXT = "Password"

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   STYLING   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   WIDGETS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label = tk.Label(self, text="Log In Page", font=('Times', '20'))

        self.usernameEntry = ttk.Entry(self)
        self.usernameEntry.insert(0, self.USERNAME_TEXT)

        self.passwordEntry = ttk.Entry(self, show="*")
        self.passwordEntry.insert(0, self.PASSWORD_TEXT)

        self.logInBtn = tk.Button(self, text="Log In", command=self._log_user_in)

        self.createAccountBtn = tk.Button(self, text="New Account", command=self._create_account)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label.pack(pady=50,padx=0)
        self.usernameEntry.pack(pady=10, padx=0)
        self.passwordEntry.pack(pady=10, padx=0)
        self.logInBtn.pack(pady=10, padx=0)
        self.createAccountBtn.pack(pady=10, padx=0)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        #self.entry.bind("<Return>", self.send_message) # binds hitting the enter key to the send_message() event handler
        self.usernameEntry.bind("<FocusIn>", self._on_username_entry_click)
        self.passwordEntry.bind("<FocusIn>", self._on_pw_entry_click) 
        self.usernameEntry.bind("<FocusOut>", self._on_focusout) 
        self.passwordEntry.bind("<FocusOut>", self._on_focusout) 
    
    def _create_account(self):
        self._reset_fields()
        self.view.show_create_account()

    # TODO: Error handling
    # logs the user in after the button is clicked 
    def _log_user_in(self):
        user_name = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if (user_name != self.USERNAME_TEXT and password != self.PASSWORD_TEXT):
            login_response = self.view.log_in(user_name, password)

            #handle login errors, if no errors reset the fields so when a user logs out their
            #info is not still in the fields
            if login_response == 401:
                messagebox.showerror("Invalid Credentials", "Invalid Username/Password")
            elif login_response == 503:
                messagebox.showerror("Connection refused", "Server is down")
            elif login_response != 200:
                messagebox.showerror("Failed to login", "Error code: " + str(login_response))
            else:
                self._reset_fields()

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

    #clear and reset fields upon window change
    def _reset_fields(self):
        self.usernameEntry.delete(0, tk.END)
        self.usernameEntry.insert(0, self.USERNAME_TEXT)
        self.passwordEntry.delete(0, tk.END)
        self.passwordEntry.insert(0, self.PASSWORD_TEXT)