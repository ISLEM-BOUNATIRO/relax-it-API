import telnetlib
tn = telnetlib.Telnet("telehack.com ")
result=tn.read_all()
tn.write(("joke"+"\n").encode('ascii') + b"\n")
result=tn.read_all().decode('ascii')
tn.write("exit\n".encode('ascii'))   
result=tn.read_all().decode('ascii')
print (result)
