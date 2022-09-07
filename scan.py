from app import app,request
from flask_socketio import SocketIO,send, emit
from flask import render_template
import asyncio
from netmiko import ConnectHandler
import regex as re
from group import *
from device import *
import os
import time
import subprocess
import threading


class rscan(object):

    state = {'online': [], 'offline': []} # Dictionary with list
    ips = [] # Should be filled by function after taking range

    # Amount of pings at the time
    thread_count = 8

    # Lock object to prevent race conditions
    lock = threading.Lock()

    # Using Windows ping command
    def ping(self, ip):
        #answer = subprocess.call(['ping','-n','4',ip],stdout = subprocess.DEVNULL)
        p = subprocess.Popen('ping -n 2 '+ip,stdout = subprocess.DEVNULL)
        p.wait()
        rslt=(p.poll()==0)
        print (ip+":  "+str(rslt))

        return rslt 


    def pop_queue(self):
        ip = None
        self.lock.acquire() # lock !!!
        if self.ips:
            ip = self.ips.pop()

        self.lock.release()
        return ip


    def noqueue(self):
        while True:
            ip = self.pop_queue()
            if not ip:
                return None
            result = 'online' if self.ping(ip) else 'offline'
            message=ip+": "+result
            socketio.send(message) 
            self.state[result].append(ip) ### check again


    def start(self):
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.noqueue)
            t.start()
            threads.append(t)
        # Wait for all threads
        [ t.join() for t in threads ]
        return self.state

    def rng(self, frm, to, ip3):
        pingable=[254,253,1,226,227,228,229,230,146,147,128]
        self.frm = frm
        self.to = to
        self.ip3 = ip3
        for i in pingable:
            ip = ip3 + str(i)
            self.ips.append(ip)


@app.route('/api/get_device_info',methods=['POST'])
def get_device_info():
    ip=request.json['ip']
    if not reachable(ip): # PINGING THE ADDRESS
        return {"result": "error " +ip+" is unreachable"}
    else:
        device=get_cisco_device_info(ip)
        device_schema = DeviceSchema()
        output = device_schema.dump(device)
        return jsonify(output)
        


socketio =SocketIO(app,cors_allowed_origins="*")
@socketio.on('scan_bp') 
def handlemsg(office_subnet):
    print('office_subnet: ', office_subnet)
    #asyncio.run(async_handler(office_subnet))
    office_subnet=office_subnet[0:len(office_subnet)-1]
    x=rscan()
    x.thread_count = 8
    x.rng(1,256,office_subnet)
    x.start()


async def async_handler(office_subnet):
    office_subnet=office_subnet[0:len(office_subnet)-2]
    for num_device in range(145,150):
        handle_ips_task = asyncio.create_task(scan_device(office_subnet+"."+str(num_device))) 
    await handle_ips_task   
    
async def scan_device(ip:str):
    message=ip+": "+str(reachable(ip))
    socketio.send(message) 


def reachable(host_ip:String):
    host_state  = True if os.system("ping -n 2 " + host_ip) is 0 else False
    return host_state

def get_cisco_device_info(ip):
    cisco = {
                'device_type': 'cisco_ios',
                'ip': ip,
                'username': 'islem',  # ssh username
                'password': 'islem',  # ssh password
            }
    try:
        net_connect = ConnectHandler(**cisco)

        # execute show version on router and save output to output object
        output = net_connect.send_command('show version')
        net_connect.disconnect()
        # finding hostname in output using regular expressions
        regex_hostname = re.compile(r'(\S+)\suptime')
        hostname = regex_hostname.findall(output)

        # finding uptime in output using regular expressions
        regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
        uptime = regex_uptime.findall(output)

        # finding version in output using regular expressions
        regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
        version = regex_version.findall(output)

        # finding serial in output using regular expressions
        regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
        serial = regex_serial.findall(output)

        # finding ios image in output using regular expressions
        regex_ios = re.compile(r'System image file is "[^"]*"')
        ios = regex_ios.findall(output)
        ios[0] = ios[0].replace("System image file is ", '')
        ios[0] = ios[0].replace('"', '')

        # finding model in output using regular expressions
        regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
        model = regex_model.findall(output)
        device = Device(ip = ip,
        firmware_version = version[0],
        model =model[0],
        serial_number = serial[0],
        type = "router or switch",
        vendor = "cisco",hostname=hostname[0])
        return device
    except Exception as e:
        if("Common causes of this problem are:" in str(e)):
            print(ip+" is unreachable")
        else:
            print(e+" catched in scan.py at the last line")
