from app import app,jsonify,request
import os
from flask_sock import Sock  
import telnetlib
sock =Sock(app)
#FOR TESTING
#wscat  -c ws://localhost:80/reverse

@sock.route('/reverse') 
def reverse(web_socket) : 
    tn = telnetlib.Telnet("telehack.com 23")
    while True: 
        command = web_socket.receive() 
        if(command=="exit"):
            web_socket.send("End of process")
            break
        text=tn.read_all()
        if(text):
            print(text)
            
        tn.write((command+"\n").encode('ascii') + b"\n")
        result=tn.read_all().decode('ascii')
        web_socket.send(result)
    tn.write("exit\n".encode('ascii'))   



    


