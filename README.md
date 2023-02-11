### Server Routes

#### Login via http get request

localhost:5000/login/<username>

logs in user (creates a session)

#### Logout via http get request

localhost:5000/logout/<username>

logs out user

#### SocketIO events

(it might not be necessary to seperate these into out/in)
(investigating, will report back)

"message_out" event

handles emitting/receiving messages from clients to server

"message_in" event

handles emitting/receiving messages from server to client

"user_change_out" event

handles emitting/receiving changes to the active user list from clients to server

"user_change_in" event

handles emitting/receiving changes to the active user list from server to client

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

Run the server (from its folder):

```sh
$ python server.py
```

Run as many clients as you'd like (from its folder):

```sh
$ python client.py
```

## Feature List

- Message a single user
  - Handled via SocketIO
  - Emits only to specific user/sender ("rooms"?)
  - Shows who message is from
  - Message is shown in group chat window for receiver
  - Message is optimistically shown for sender
    - When the sender receives the message back, they know it was a success (do not re-add it to their list)
    - If they do not receive a response after a certain time or are disconnected, mark the message as not sent (maybe change text color)
    - Returns error if user does not exist (mark red)
  - Uses information (sender, receiver, message_id (auto-incremented on server), message_text)
  - Messages are not persistent
- Send message to group
  - Handled via SocketIO
  - Uses information (sender, receiver [marked as "group"], message_id (auto-incremented on server), message_text)
  - Appears in group chat window
  - Message is shown in group chat window for receiver
    - Message is optimistically shown for sender
      - When the sender receives the message back, they know it was a success (do not re-add it to their list)
      - If they do not receive a response after a certain time or are disconnected, mark the message as not sent (maybe change text color)
    - Messages are not persistent
- Login via https
  - Currently a user will login simply by submitting their username and password (password is ignored for now)
  - Users currently are non-persistent
  - Cannot login with username that already is logged in
  - Cannot only connect via SocketIO after creating a valid login session
  - Future features
    - Oauth?
    - There is no registration, users use google account
    - Last how long?
- Logout vias https
- Display list of active users
  - Handled via SocketIO
  - Active users appear when they connect via SocketIO
  - Users dissapear when they logout
  - Users dissapear when their SocketIO connection ends after a certain grace period
