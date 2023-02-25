import tkinter as tk
from tkinter import ttk

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
        self.logInBtn = tk.Button(self, text="Log In")


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
        self.usernameEntry.bind("<FocusIn>", self.on_username_entry_click) # gets rid of the "Enter text here..." when clicking into the Entry
        self.usernameEntry.bind("<FocusOut>", self.on_focusout) # brings back the "Enter text here..." when clicking off of the Entry
        self.passwordEntry.bind("<FocusIn>", self.on_pw_entry_click) # gets rid of the "Enter text here..." when clicking into the Entry
        self.passwordEntry.bind("<FocusOut>", self.on_focusout) # brings back the "Enter text here..." when clicking off of the Entry

    def on_username_entry_click(self, event):
        if self.usernameEntry.get() == self.USERNAME_TEXT:
            self.usernameEntry.delete(0, "end")

    def on_pw_entry_click(self, event):
        if self.passwordEntry.get() == self.PASSWORD_TEXT:
            self.passwordEntry.delete(0, "end")
    
    def on_focusout(self, event):
        if self.usernameEntry.get() == "":
            self.usernameEntry.insert(0, self.USERNAME_TEXT)
        
        if self.passwordEntry.get() == "":
            self.passwordEntry.insert(0, self.PASSWORD_TEXT)
    
    # helper method that gets called when the user presses the log-in button
    def log_user_in(self, event=None):
        pass

    # def create_menubar(self, parent):
    #     menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

    #     # creates a settings menu
    #     settings_menu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
    #     menubar.add_cascade(label="Settings", menu=settings_menu)
    #     settings_menu.add_command(label="NextFrame", command=lambda: parent.show_frame(parent.LogInPage))
    #     settings_menu.add_command(label="Home", command=lambda: parent.show_frame(parent.ChatPage))
    #     settings_menu.add_command(label="Close", command=lambda: parent.show_frame(parent.ChatPage))
    #     settings_menu.add_separator()
    #     settings_menu.add_command(label="Exit", command=parent.quit)  

    #     # BUG -----------------------------------------------------------------------------------------------------------
    #     processing_menu = Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="Validation", menu=processing_menu)
    #     processing_menu.add_command(label="validate")
    #     processing_menu.add_separator()

    #     ## help menu
    #     help_menu = Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="Help", menu=help_menu)
    #     help_menu.add_command(label="About", command=utils.about)
    #     help_menu.add_separator()

    #     return 