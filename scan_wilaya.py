import subprocess
import threading
import device
import office
import scan 
import scan_office
class scan_wilaya(object):
    ips = [] 
    pingable_offices=[]
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

    def scan_pingables(self):
        while True:
            ip = self.pop_ip_from_list()
            if not ip:
                return None
            if self.ping(ip+str(254)):
                self.pingable_offices.append(ip+str(0))
                message = ip+str(254)+' is a pingable firewall' 
                scan.socketio.send(message)
            elif self.ping(ip+str(1)):
                self.pingable_offices.append(ip+str(0))
                message = ip+str(1)+' is a pingable router' 
                scan.socketio.send(message)
            else:
                message = ip+str(0)+' is a unreachable' 
                scan.socketio.send(message)
             


    def start(self):
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.scan_pingables)
            t.start()
            threads.append(t)
        # Wait for all threads
        [ t.join() for t in threads ]
        scan.socketio.send("Scanning offices")
        threads = []
        for office_subnet2 in self.pingable_offices:
            scan.socketio.send("Scanning office  "+str(office_subnet2))
            office_subnet2=office_subnet2[0:len(office_subnet2)-1]
            ip_list=[254,253]
            #1,226,227,228,229,230
            x=scan.scan_office_and_devices()
            x.thread_count = 8
            x.init_ip_list(ip_list,office_subnet2)
            x.start()            

        return self



