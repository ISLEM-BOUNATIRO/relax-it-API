import subprocess
import threading
import device
import office
import scan 
class scan_office_and_devices(object):
    last_office=False
    rana_f_office=True
    ips = [] 
    thread_count = 256
    lock = threading.Lock()
    def ping(self, ip):
        output=""
        p = subprocess.Popen('ping -n 2 '+ip,stdout=subprocess.PIPE)
        output = p.stdout.read()
        p.wait()
        #result=(p.poll()==0) 
        result="Approximate round trip" in str(output)
        return result 
    def pop_ip_from_list(self):
        ip = None
        self.lock.acquire() # lock !!!
        if self.ips:
            ip = self.ips.pop(0)
        self.lock.release()
        return ip
    progress=0
    number=0    
    number_of_ips=1
    def scan_add_devices(self):
        
        while True:
            ip = self.pop_ip_from_list()
            if not ip:
                return None
            pingable =self.ping(ip)

            if(pingable):
                message=ip+" is pingable"
                scan.socketio.send(message) 
                d=-1
                if(scan.get_device_type(ip)=="Firewall"):
                    d=scan.get_fortinet_info(ip)
                elif(scan.get_device_type(ip)=="Router"):
                    d=scan.get_cisco_device_info(ip,"admin","admin")
                elif(scan.get_device_type(ip)=="Switch"):
                    d=scan.get_cisco_device_info(ip,"admin","admin")
                    #LOOP OVER ALL USERNAMES UNTIL U GET THE RIGHT ONE
                    #d=scan.get_cisco_device_info(ip,"admin","admin")
                    #GET_SWITCH_VENDOR()
                    #d=scan.get_cisco_device_info(ip,"cisco","cisco")
                    #for now 3ndna ghir fiberhome
                    #if(ip=="10.117.5.226"):
                    #    d=scan.get_fiberhome_info(ip,"admin","12345")
                    
                if(d!=-1):
                    result=device.add_device(d)["result"]
                    if (result=="1"):
                        message=ip+" was added to database"
                        scan.socketio.send(message)
                    else:
                        message= result
                        scan.socketio.send(message) 
                    spli=d.hostname.split("-")
                    off_name=spli[1] +" "+spli[2]
                    spli=ip.split('.')
                    off_subnet=spli[0]+"."+spli[1]+"."+spli[2]+".0"
                    off = office.Office(office_subnet= off_subnet,name= off_name)
                    
                    #replace later with get_device_type
                    fourth_byte=ip.split('.')[3]
                    a=(fourth_byte=="254")
                    b=(fourth_byte=="1")
                    if a | b:
                        result_office=office.add_office(off)
                        if(result_office["result"]=="1"):
                            scan.socketio.send("Office "+str(off.name)+" added to database")
                else:
                    message="attention "+ip+" is pingable but not reachable"
                    scan.socketio.send(message)
            self.number=self.number+1
            self.progress=int(( self.number/self.number_of_ips)*100)
            message ="Scanning office " +str(self.progress)+" %" 
            if(self.rana_f_office):
                scan.socketio.send(message)                

    def start(self):
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.scan_add_devices)
            t.start()
            threads.append(t)
        # Wait for all threads
        [ t.join() for t in threads ]
        if(self.rana_f_office):
            scan.socketio.send("Operation Finished")
        if(self.last_office):
            scan.socketio.send("Scanning offices 100 %" )
            scan.socketio.send("Operation Finished")
        return self
    def init_ip_list(self, ip_list, ip3):
        self.ip3 = ip3
        self.number_of_ips=len(ip_list)
        for i in ip_list:
            ip = ip3 + str(i)
            self.ips.append(ip)


