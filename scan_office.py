import subprocess
import threading
import device
import office
import scan 
class scan_office_and_devices(object):

    ips = [] 
    thread_count = 8
    lock = threading.Lock()
    def ping(self, ip):
        p = subprocess.Popen('ping -n 2 '+ip,stdout = subprocess.DEVNULL)
        p.wait()
        result=(p.poll()==0)
        print (ip+":  "+str(result))
        return result 
    def pop_ip_from_list(self):
        ip = None
        self.lock.acquire() # lock !!!
        if self.ips:
            ip = self.ips.pop()
        self.lock.release()
        return ip

    def scan_add_devices(self):
        while True:
            ip = self.pop_ip_from_list()
            if not ip:
                return None
            result = 'pingable' if self.ping(ip) else 'offline'
            message=ip+" is "+result
            scan.socketio.send(message) 
            d=scan.get_cisco_device_info(ip)
            result=device.add_device(d)["result"]
            if (result=="1"):
                message=ip+" was added to database"
            else:
                message= result
            scan.socketio.send(message) 

            off = office.Office(office_subnet= ip,name= d.hostname)
            fourth_byte=ip.split('.')[3]
            
            a=(fourth_byte=="254")
            b=(fourth_byte=="1")
            if a | b:
                result_office=office.add_office(off)
                if(result_office["result"]=="1"):
                    scan.socketio.send("Office "+str(off.name)+" added to database")


    def start(self):
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.scan_add_devices)
            t.start()
            threads.append(t)
        # Wait for all threads
        [ t.join() for t in threads ]
        scan.socketio.send("Operation Finished")
        return self
    def init_ip_list(self, ip_list, ip3):
        self.ip3 = ip3
        for i in ip_list:
            ip = ip3 + str(i)
            self.ips.append(ip)


