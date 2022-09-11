import telnetlib
hostname="C1841-Alger-5"
device_type='Cisco'
ip ="192.168.217.253"
username="admin"
password="admin"
commands = ["conf t","hostname milou","hostname C1841-Alger-5","end"]

def excute_script(ip,username,password,commands):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username: ")
    tn.write(username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"terminal length 0\n")
    tn.read_until(b"#terminal length 0\r")     
    
    for i in range(len(commands)):
        command = str(commands[i])+"\n"
        tn.write(command.encode('ascii'))
    tn.write(b"exit\n")
    return tn.read_all().decode('ascii')
    



























 
#---------------------------------------------------------
class pp:
    def is_big():
        return True
tn=telnetlib.Telnet("192.168.217.254")
tn.read_until(b"login: ")
tn.write("admin".encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write("admin".encode('ascii') + b"\n")
while (pp.is_big()):
    command=input()
    command=command+"\n"
    tn.write(command.encode('ascii'))
    tn.write("endeocrino\n".encode('ascii'))
    output=tn.read_until(b"# endeocrino\r\r\nUnknown action 0").decode('ascii')
    output=output.split('\n')
    output=output[1:-2]
    last_output=""
    for line in output:
        last_output=last_output+"\n"+line
    print(last_output)






