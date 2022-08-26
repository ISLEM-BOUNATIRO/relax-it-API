
from netmiko import ConnectHandler
import telnetlib
import os
from app import app,jsonify,request
from time import sleep
wait=0.1

def ftl(filename):
    dirname = os.path.dirname(__file__)
    filename_full = os.path.join(dirname, "Scripts/"+filename+".txt")
    f = open(filename_full, "r")
    return  f.read().split("\n")


def transport_input_all(host,username,password,netmiko_device_type):
    myrouter = {
        'device_type':netmiko_device_type,
        'ip': host,
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**myrouter)
    output = net_connect.send_command('show run')
    if "transport input all" in output:
        return True
    else:
        return False

def disable_telnet(host,username,password,netmiko_device_type):   
    
    myrouter = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': username,
        'password': password,
    }

    net_connect = ConnectHandler(**myrouter)
    config_commands = ftl("DISABLE_TELNET")
    output = net_connect.send_config_set(config_commands)
    

def ssh_is_enabled(HOST,password):
    tn = telnetlib.Telnet(HOST)
    sleep(wait)              # wait for greeter
    tn.read_very_eager(); 
    tn.write(password.encode('ascii') + b"\n")
    tn.write("enable\n".encode('ascii'))   
    tn.write((password+"\n").encode('ascii'))
    tn.write("sh ip ssh\n".encode('ascii')) 
    tn.write("exit\n".encode('ascii'))    

    result=tn.read_all().decode('ascii')
    
    if "Disabled" in result:
        return False
    else:
        return True


def enable_ssh(HOST,user,password):
    tn = telnetlib.Telnet(HOST)
    sleep(wait)             
    tn.read_very_eager()
    tn.write(password.encode('ascii') + b"\n")
    tn.write("enable\n".encode('ascii'))   
    tn.write((password+"\n").encode('ascii'))

    commands = ftl("ENABLE_SSH")
    for i in range(len(commands)):
        c = str(commands[i])+"\n"
        tn.write(c.encode('ascii'))
    tn.write(b"exit\n")
    tn.read_all().decode('ascii')
     


@app.route('/api/enable_ssh_disable_telnet',methods=['POST'])
def enable_ssh_disable_telnet_api():
    ip = request.json['ip']
    return enable_ssh_disable_telnet(ip)

def enable_ssh_disable_telnet(ip):
    user = password = "islem"
    host=ip
    telnet_state =""
    ssh_state="ENABLED"
    #CONNECTION AVEC TELNET POUR ACTIVER SSH
    try:
        enabled=ssh_is_enabled(host,password)
        
        if (enabled==False):
            
            enable_ssh(host,user,password)
            
            ssh_state="GOT ACTIVATED"
            print("ssh got activated")
         
        else:
            ssh_state="WAS ALREADY ACTIVATED"
            print("WAS ALREADY ACTIVATED")
            
    except Exception as exception:
        s="No connection could be made because the target machine actively refused it"
        if s in str(exception):
            telnet_state="UNREACHABLE"
        print("first exception ="+str(exception))
    #CONNECTION AVEC SSH POUR (TRANSPORT INPUT SSH) ONLY
    try:
         
        all=transport_input_all(host,user,password, 'cisco_ios')
        if(all):
            print("transport_input_all is true")
            disable_telnet(host,user,password, 'cisco_ios')
            telnet_state=telnet_state+" GOT DISABLED"
            print("telnet got disabled")
            
        else:
            
            telnet_state=telnet_state+" ALREADY DISABLED"
            print("telnet allready disabled")
            
    except Exception as exception:
        ssh_state=ssh_state+",UNREACHABLE"
        print("second exception ="+str(exception))
    return {"telnet":telnet_state,"ssh":ssh_state}