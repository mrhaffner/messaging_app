## Proof of Concept

### Server Routes

#### Login via http get request

localhost:5000/login/<username>

logs in user (creates a session)

#### Logout via http get request

localhost:5000/logout/<username>

logs out user

#### Persistent connection via SocketIO

processes text events labeled "message", prints to console, and rebroacasts the message as a "receive" event to all connected clients

### Client

Prompts user for "username", logs them in via session

Connects to localhost:5000 via SocketIO

Prints "receive" events to console

Will take message input via console and emit "message" event to server until "x" is entered into console.

## Set Up

(This is for linux/mac, if you are using Windows you are on your own)

Install Python and add to Path (author is using 3.9)

Create/activate a virtual environment so you are not installing packages globally:

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
$ python server.py
```

Run as many clients as you'd like:

```sh
$ python client.py
```
