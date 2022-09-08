import telnetlib
import regex as re
def show_version_fiberhome_telnet(ip,hostname,password):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username: ")
    tn.write(hostname.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"show version\n")
    output=tn.read_until(b"System Memory").decode('ascii')
    tn.write(b"exit\n")
    try:
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
        lista=[version[0].rstrip(),serial[0].rstrip(),model[2].rstrip()]#
        return lista
    except Exception as e:
        return str(e)+"\n"+output

p=show_version_fiberhome_telnet("10.117.5.226","admin","12345")
print(p)
       