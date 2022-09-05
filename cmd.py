from app import app
from flask_socketio import SocketIO,send, emit
from flask import render_template
import asyncio
socketio =SocketIO(app,cors_allowed_origins="*")

from datetime import datetime

import time

# @socketio.on('message') 
# def handlemsg(msg): 
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
    
#     socketio.send(current_time) 
#     time.sleep(1)


async def say_after(ip:str):
    socketio.send(ip)
    print(ip)

async def async_handler(msg):
    for nbr in msg:
        handle_ips_task = asyncio.create_task(say_after(nbr))
        await handle_ips_task
        time.sleep(3)



    


@socketio.on('message') 
def handlemsg(msg):
    print('message: ', msg)
    # print(type(msg))
    asyncio.run(async_handler(msg))

    


@app.route("/") 
def main(): 
    return render_template("main.html")