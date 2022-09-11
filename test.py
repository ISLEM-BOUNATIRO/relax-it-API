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
    

print(excute_script(ip,username,password,commands))