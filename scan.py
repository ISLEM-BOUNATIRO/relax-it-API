from app import *
from scan_office  import *
from flask_socketio import SocketIO,send, emit
from flask import render_template
import asyncio
from netmiko import ConnectHandler
import regex as re
import os

socketio =SocketIO(app,cors_allowed_origins="*")
@socketio.on('scan_bp') 
def handlemsg(office_subnet):
    #asyncio.run(async_handler(office_subnet))
    socketio.send("Scanning office  "+str(office_subnet))
    office_subnet=office_subnet[0:len(office_subnet)-1]
    ip_list=[254,253]
    #1,226,227,228,229,230
    x=scan_office_and_devices()
    x.thread_count = 8
    x.init_ip_list(ip_list,office_subnet)
    x.start()
@socketio.on('disconnect') 
def handledisco():
    print('SOCKET CLOSED')

@socketio.on('scan_wilaya') 
def handledisco(wilaya_number):
    socketio.send("Scanning wilaya number "+str(wilaya_number))
    office_subnet_list=[]
    second_byte=int(wilaya_number)+64
    for third_byte in range(1,256):
        office_subnet_list.append("192."+str(second_byte)+"."+str(third_byte)+".0")
        print(office_subnet_list[third_byte-1])
    
    



    
    


async def async_handler(office_subnet):
    office_subnet=office_subnet[0:len(office_subnet)-2]
    for num_device in range(145,150):
        handle_ips_task = asyncio.create_task(scan_device(office_subnet+"."+str(num_device))) 
    await handle_ips_task   
    
async def scan_device(ip:str):
    message=ip+": "+str(reachable(ip))
    socketio.send(message) 


def reachable(host_ip):
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
