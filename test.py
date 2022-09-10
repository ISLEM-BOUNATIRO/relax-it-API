from netmiko import *
from netmiko import ConnectHandler

#TO EXECUTE JUST ONE COMMAND
#output = net_connect.send_command('get system status')

def get_netmiko_device_type(ip):
    if(ip.split('.')[3]=="254"):
        return "fortinet"
        
    return 'cisco_ios'

def execute_config_ssh(ip,username,password):   
    myrouter = {
        'device_type': get_netmiko_device_type(ip),
        'ip': ip,
        'username': username,
        'password': password,
    }

    net_connect = ConnectHandler(**myrouter)
    config_commands = "hostname C1841-Alger-5"
    output = net_connect.send_config_set(config_commands)
    print(output)

hostname="C1841-Alger-5"
device_type='Cisco'
ip ="192.168.217.253"
username="admin"
password="admin"
#execute_config_ssh(ip,username,password)

mydevice = {
    'device_type': get_netmiko_device_type(ip),
    'ip': ip,
    'username': username,
    'password': password,
} 

net_connect = ConnectHandler(**mydevice)
command = "show"

net_connect.enable()
net_connect.find_prompt() + "\n"

output = net_connect.send_command(command)



print(output)