from netmiko import ConnectHandler

myFirewall = {
    'device_type': 'fortinet',
    'ip': '192.168.217.136',
    'username': 'admin',
    'password': 'islem',
}

net_connect = ConnectHandler(**myFirewall)
output = net_connect.send_command('get system status')
print(output)
