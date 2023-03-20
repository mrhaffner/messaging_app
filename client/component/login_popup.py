import tkinter as tk
from tkinter import ttk
from controller import *
from component.main_window import ChatPage

# displays the login form
class LoginPopup(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

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

        # MISSING command to call handler to log in
        self.logInBtn = tk.Button(self, text="Log In", command=self.on_button_click)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   GRID CONFIGURATIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        self.label.pack(pady=50,padx=0)
        self.usernameEntry.pack(pady=10, padx=0)
        self.passwordEntry.pack(pady=10, padx=0)
        self.logInBtn.pack(pady=10, padx=0)

        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~   BINDINGS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
        #self.entry.bind("<Return>", self.send_message) # binds hitting the enter key to the send_message() event handler
        self.usernameEntry.bind("<FocusIn>", self.on_username_entry_click)
        self.passwordEntry.bind("<FocusIn>", self.on_pw_entry_click) 
        self.usernameEntry.bind("<FocusOut>", self.on_focusout) 
        self.passwordEntry.bind("<FocusOut>", self.on_focusout) 
    
    def on_button_click(self):
        if (self.usernameEntry.get() != self.USERNAME_TEXT and self.passwordEntry.get() != self.PASSWORD_TEXT):
            print('first check')
            if (login(self.usernameEntry.get(), self.passwordEntry.get())):
                print('user logged in')
                # switch page to ChatPage - not sure if there is a better way to do this or if this is even correct
                chat_page = ChatPage
                chat_page.tkraise() 

    # gets rid of the "Enter text here..." when clicking into the Entry
    def on_username_entry_click(self, event):
        if self.usernameEntry.get() == self.USERNAME_TEXT:
            self.usernameEntry.delete(0, "end")

    # gets rid of the "Enter text here..." when clicking into the Entry
    def on_pw_entry_click(self, event):
        if self.passwordEntry.get() == self.PASSWORD_TEXT:
            self.passwordEntry.delete(0, "end")
    # brings back the "Enter text here..." when clicking off of the Entry
    def on_focusout(self, event):
        if self.usernameEntry.get() == "":
            self.usernameEntry.insert(0, self.USERNAME_TEXT)
        
        if self.passwordEntry.get() == "":
            self.passwordEntry.insert(0, self.PASSWORD_TEXT)
    
    # helper method that gets called when the user presses the log-in button
    def log_user_in(self, event=None):
        pass
