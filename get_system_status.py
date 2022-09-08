from netmiko import ConnectHandler
import regex as re

#GOOGLE REGEX GENERATOR
def get_device_type(ip):
    fourth_byte=ip.split('.')[3]
    if (fourth_byte=="253" or fourth_byte=="1"):
        return "Router"
    if (fourth_byte=="254"):
        return "Firewall"
    return "Switch"

ip='10.117.5.254'
myFirewall = {
    'device_type': 'fortinet',
    'ip': ip,
    'username': 'admin',
    'password': 'admin12345',
}

net_connect = ConnectHandler(**myFirewall)
output = net_connect.send_command('get system status')

# hostname
regex_hostname = re.compile(r'Hostname:\s(\S+)')
hostname = regex_hostname.findall(output)
# version 
regex_version = re.compile(r'Version:\s(\S+)')
version = regex_version.findall(output)
# serial
regex_serial = re.compile(r'Serial-Number:\s(\S+)')
serial = regex_serial.findall(output)
#ios image
regex_ios = re.compile(r'Serial-Number:\s(\S+)')
ios = regex_ios.findall(output)
#model
regex_model = re.compile(r'Version:\s(.+)')
model = regex_model.findall(output)

lista=[hostname[0],version[0],model[0],serial[0]]
for e in lista:
    print(e)
