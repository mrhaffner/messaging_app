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

## Set Up

### For Windows

Install Python (author is using 3.9)

Create/activate a virtual environment so you are not installing packages globally (optional):

```sh
$ py -m venv env
$ source env/Scripts/activate
```

Install the required packages

```sh
$ pip install -r requirements.txt
```

Run the server:

```sh
$ python server/main.py
```

Run as many clients as you'd like:

```sh
$ python client/main.py.py
```

### For Linux/Mac

Install Python (author is using 3.9)

Create/activate a virtual environment so you are not installing packages globally (optional):

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Install the required packages

```sh
$ pip install -r requirements.txt
```

Run the server:

```sh
$ python server/main.py
```

Run as many clients as you'd like:

```sh
$ python client/main.py
```
