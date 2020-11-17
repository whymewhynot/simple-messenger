import time
import sqlite3
import os
from flask import Flask, request, Response

import settings

app = Flask(__name__)
app.config.from_object(settings)


@app.route("/send", methods=["POST"])
def send():
    name = request.json.get("name")
    text = request.json.get("text")
    message_time = time.time()
    if not name or not text:
        return Response(status=400)

    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        qs = "INSERT INTO messages VALUES (?,?,?)"
        c.execute(qs, (name, message_time, text))
        conn.commit()

    return Response(status=200)


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args["after"])
    except:
        return Response(status=400)

    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        try:
            qs = f"SELECT * FROM messages WHERE datetime > {after} ORDER BY datetime DESC"
            response = cursor.execute(qs)

            messages = [{'name': r[0], 'time': r[1], 'text': r[2]} for r in response]
        except:
            messages = []

    return {"messages" : messages}



@app.route("/")
def index():
    return "Hello, World! This is simple Python messenger"

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        try:
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                                                  name TEXT NOT NULL,
                                                  datetime REAL NOT NULL,
                                                  message TEXT NOT NULL                                              
                                                  );
                            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"An error occur during database initializing: {e}")

    app.run()