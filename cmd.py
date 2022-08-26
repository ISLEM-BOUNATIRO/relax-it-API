from app import app
from flask_socketio import SocketIO,send, emit
from flask import render_template
socketio =SocketIO(app)

from datetime import datetime

import time

@socketio.on('message') 
def handlemsg(msg): 
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        socketio.send(current_time) 
        time.sleep(1)
    

@app.route("/") 
def main(): 
    return render_template("main.html")