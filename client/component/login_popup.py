import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext

# displays the login form
class LoginPopup(ttk.Frame):
    # def __init__(self, parent, container):
    #     super().__init__(container)
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="Log In Page", font=('Times', '20'))
        label.pack(pady=0,padx=0)

        # MISSING command to call handler to log in
        logInBtn = tk.Button(self, text="Log In")
        logInBtn.pack(pady=0, padx=0)

        ## ADD CODE HERE TO DESIGN THIS PAGE

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