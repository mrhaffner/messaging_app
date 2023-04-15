## Messaging App

A chat application that allows users to send public messages to a group or private messages to a specific user.

Features:

- User GUI
- User registration
- User login / logout
- Users are saved to text based database by server
- Send a public message to all logged in users
- Send a private message to one logged in user
- Admin super user may kick users from chat
- GUI displays a list of all logged in users

## Contents

```
├── README.md  (you are here)
├── presentation.pptx  (slides for our project presentation)
├── writeup.docx  (our project write up)
├── client  (the client application - MVC architecture)
│   ├── component  (GUI components)
│   │   ├── __init__.py  (denotes a Python package)
│   │   ├── create_account_popup.py  (create account page)
│   │   ├── login_popup.py  (login page)
│   │   └── main_window.py  (main page)
│   ├── controller.py  (the client controller)
│   ├── main.py  (entry to the app)
│   ├── model  (the models used)
│   │   ├── __init__.py  (denotes a Python package)
│   │   ├── message.py  (models related to messages)
│   │   ├── shared.py  (shared parent classes)
│   │   └── user.py  (models related to the user)
│   └── view.py  (the client view)
├── prototype  (the prototype used when designing this project)
│   ├── README.md  (original readme)
│   ├── client.py  (client prototype)
│   └── server.py  (server prototype)
└── server  (the server application)
    ├── main.py  (the server entry point)
    └── model  (the models used)
        ├── __init__.py  (denotes a Python package)
        ├── message.py  (models related to messages)
        └── user.py  (models related to the user)
```

## Set Up

### For Linux/Mac

Install Python (author is using 3.9)

Create/activate a virtual environment so you are not installing packages globally (optional):

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Install the required packages (assuming python 3.6 for the university computers)

```sh
$ sudo apt-get install python3.6-tk
$ pip install requests
$ pip install flask
$ pip install flask-socketio
$ pip install "python-socketio[client]"
```

Run the server:

```sh
$ python server/main.py
```

Run as many clients as you'd like:

```sh
$ python client/main.py
```
