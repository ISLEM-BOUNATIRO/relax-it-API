from app import *
from scan_office  import *
from flask_socketio import SocketIO,send, emit
from flask import render_template
import asyncio
from netmiko import ConnectHandler
import regex as re
import os
import scan_wilaya as sw
import telnetlib
socketio =SocketIO(app,cors_allowed_origins="*")
@socketio.on('scan_bp') 
def handlemsg(office_subnet):
    #asyncio.run(async_handler(office_subnet))
    socketio.send("Scanning office  "+str(office_subnet))
    office_subnet=office_subnet[0:len(office_subnet)-1]
    ip_list=[254,253,1,226,227,228,229,230]
    #1,226,227,228,229,230
    x=scan_office_and_devices()
    x.thread_count = 256
    x.init_ip_list(ip_list,office_subnet)
    x.start()
@socketio.on('disconnect') 
def handledisco():
    print('SOCKET CLOSED')

@socketio.on('scan_wilaya') 
def handledisco(wilaya_number):
    socketio.send("Pinging offices of wilaya number "+str(wilaya_number))
    office_subnet_three_bytes=[]
    second_byte=int(wilaya_number)+64
    for third_byte in range(1,256):#ATTENTIOOOOON
        office_subnet_three_bytes.append("10."+str(second_byte)+"."+str(third_byte)+".")
        #print(office_subnet_three_bytes[third_byte-1])
    
    x=sw.scan_wilaya()
    x.thread_count = 256
    x.ips=office_subnet_three_bytes
    x.start()
    
    



    
    


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
def get_device_type(ip):
    lista=["226","227","228","229","230"]
    fourth_byte=ip.split('.')[3]
    if (fourth_byte=="253" or fourth_byte=="1"):
        return "Router"
    if (fourth_byte=="254"):
        return "Firewall"
    if (fourth_byte in lista):
        return "Switch"
    return ""


def get_cisco_device_info(ip,username,password):
    cisco = {
                'device_type': 'cisco_ios',
                'ip': ip,
                'username': username,  # ssh username
                'password': password,  # ssh password
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
        type = get_device_type(ip),
        vendor = "Cisco",hostname=hostname[0])
        return device
    except Exception as e:
        if("Common causes of this problem are:" in str(e)):
            print(ip+" is unreachable")
            return -1
        else:
            print(e+"\n\n\n\n catched in scan.py at the last line")
            return -1

def get_fortinet_info(ip):
    #GOOGLE REGEX GENERATOR
    fortinet = {
                'device_type': 'fortinet',
                'ip': ip,
                'username': 'admin',  # ssh username
                'password': 'admin12345',  # ssh password
            }

    try:
        net_connect = ConnectHandler(**fortinet)
        # execute show version on router and save output to output object
        output = net_connect.send_command('get system status')
        net_connect.disconnect()
        # finding hostname in output using regular expressions
        # hostname
        regex_hostname = re.compile(r'Hostname:\s(\S+)')
        hostname = regex_hostname.findall(output)
        # version 
        regex_version = re.compile(r'Version:\s(.+)')
        version = regex_version.findall(output)
        # serial
        regex_serial = re.compile(r'Serial-Number:\s(\S+)')
        serial = regex_serial.findall(output)
        #ios image
        regex_ios = re.compile(r'Serial-Number:\s(\S+)')
        ios = regex_ios.findall(output)
        #model
        regex_model = re.compile(r'Version:\s(\S+)')
        model = regex_model.findall(output)
        device = Device(ip = ip,
        firmware_version = version[0],
        model =model[0],
        serial_number = serial[0],
        type = "Firewall",
        vendor = "Fortinet",hostname=hostname[0])
        return device
    except Exception as e:
        if("Common causes of this problem are:" in str(e)):
            print(ip+" is unreachable")
            return -1
        else:
            print(e+"\n\n\n\n catched in scan.py at the last line")
            return -1
def show_version_fiberhome_telnet(ip,username,password):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username: ")
    tn.write(username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"show version\n")
    ret=tn.read_until(b"System Memory").decode('ascii')
    tn.write(b"exit\n")
    return str(ret)

def get_fiberhome_info(ip,username,password):
    try:
        output = show_version_fiberhome_telnet(ip,username,password)
        # version 
        regex_version = re.compile(r'\s\sUSP\s\(R\)\sSoftware\sVersion\s(.+)')
        version = regex_version.findall(output)
        version[0].replace('\r',' ')
        # serial
        regex_serial = re.compile(r'\s\sSerial\sNumber\s\s\s\s:\s(\S+)')
        serial = regex_serial.findall(output)
        #model
        regex_model = re.compile(r'FiberHome\s(.+)')
        model = regex_model.findall(output)
        # hostname TODOOOOOOOOOOOOO
        # regex_hostname = re.compile(r'Hostname:\s(\S+)')
        # hostname = regex_hostname.findall(output)
        # FIND EQUIVALENT sh run | in hostname FOR FIBERHOME
        device = Device(ip = ip,
        firmware_version = version[0].rstrip(),
        model =model[2].rstrip(),
        serial_number = serial[0].rstrip(),
        type = "Switch",
        vendor = "Fiberhome",hostname="TO DO")
        return device
    except Exception as e:
        if("Common causes of this problem are:" in str(e)):
            print(ip+" is unreachable")
            return -1
        else:
            print(e+"\n\n\n\n catched in scan.py at the last line")
            return -1


