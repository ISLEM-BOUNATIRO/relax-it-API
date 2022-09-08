from netmiko import ConnectHandler

myFirewall = {
    'device_type': 'fortinet',
    'ip': '10.117.5.254',
    'username': 'admin',
    'password': 'admin12345',
}

net_connect = ConnectHandler(**myFirewall)
output = net_connect.send_command('get system status')
print(output)
