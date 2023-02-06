## Proof of Concept

### Server Routes

#### Login via http get request

localhost:5000/login/<username>

logs in user (creates a session)

#### Logout via http get request

localhost:5000/logout/<username>

logs out user

#### Get list of logged in users via http get request (should be handled via websockets real time)

localhost:5000/list-users

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

## Proposed Feature List

### Core Functionalities

- Message a single user
  - Handled via websockets
  - Emits only to specific user (handled via SocketIO "rooms"?)
  - Shows who message is from
  - Returns error if user offline
  - Message is shown in group chat window prepended from (from_user_name) or in individual window?
  - Uses information (from_user, to_user, message_id (auto-increment), message_text, timestamp)
  - Messages are not persistent
- Send message to group
  - Handled via websockets
  - Uses information (from_user, message_id (auto-increment), message_text, timestamp)
  - Appears in group chat window
  - Only appears in message window for sender once emitted from backend (otherwise show an error) or is optimistically added with an error appearing on send failure (front-end filter duplicate message IDs? since it is emitted back from back end?)?
  - Messages are not persistent
- Login via https
  - Oauth?
  - There is no registration, users use google account
  - Last how long?
  - Cannot only connect via websockets after authentication?
- Logout vias https
- Display list of active users
  - Handled via websockets
  - Active users appear when they connect via websockets
  - Users dissapear when they logout
  - Users dissapear when their websocket connection ends after a certain grace period
