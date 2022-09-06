from app import app
from flask_socketio import SocketIO,send, emit
from flask import render_template
import asyncio
socketio =SocketIO(app,cors_allowed_origins="*")


async def say_after(ip:str):
    socketio.send(ip)
    print(ip)

async def async_handler(msg):
    for nbr in msg:
        handle_ips_task = asyncio.create_task(say_after(nbr))
        await handle_ips_task
        

@socketio.on('message') 
def handlemsg(msg):
    print('message: ', msg)
    asyncio.run(async_handler(msg))

