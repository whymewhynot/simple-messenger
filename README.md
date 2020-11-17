# Simple messenger
A simple messenger using Flask, SQLite and PyQt5.

### Overview ###
Flask-based ``server.py`` handles POST and GET requests from ``messenger.py`` clients: saves new messages to the database and sends updates to users accordingly. SQLite is used to store messages. PyQt5 is used for the the messenger interface.

### How to start the project ###
* Install required packages: ``pip install -r requirements.txt``
* Run the server: ``python server.py``
* Run the client: ``python messenger.py``
