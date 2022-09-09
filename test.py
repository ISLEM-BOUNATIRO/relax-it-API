import getpass
import telnetlib
import time
device_ip = "192.168.217.253"
username = "admin"
password = "admin"
command="show version"
def telnet_command(device_ip,username,password,command):
    tn = telnetlib.Telnet(device_ip)
    tn.read_until(b"Username: ")
    tn.write(username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"terminal length 0\n")
    tn.read_until(b"#terminal length 0\r")
    command=command+"\n"
    tn.write(command.encode('ascii'))
    tn.write(b"byebye\n")

    output=(tn.read_until(b'#byebye').decode('ascii'))
    output=output.split('\n')
    output=output[1:-2]
    last_output=""
    for line in output:
        last_output=last_output+"\n"+line
    return last_output

print(telnet_command(device_ip,username,password,command))