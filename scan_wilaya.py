import subprocess
import threading
import device
import office
import scan 
import scan_office
class scan_wilaya(object):
    ips = [] 
    pingable_offices=[]
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
    def scan_pingables(self):
        self.pingable_offices=[]
        
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
            self.number=self.number+1
            self.progress=int(( self.number/255)*100)
            message ="pinging offices subnets " +str(self.progress)+' %' 
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
        offices_number=len(self.pingable_offices)
        current_office=0
        for office_subnet2 in self.pingable_offices:
            current_office=current_office+1
            self.progress=int(( current_office/offices_number)*100)
            
            if(self.progress!=100):
                message ="Scanning offices " +str(self.progress)+' %' 
                scan.socketio.send(message)
            scan.socketio.send("Scanning office  "+str(office_subnet2))
            
            office_subnet2=office_subnet2[0:len(office_subnet2)-1]
            ip_list=[254,253,1]
            #1,226,227,228,229,230
            x=scan.scan_office_and_devices()
            x.last_office=(office_subnet2+"0"==self.pingable_offices[len(self.pingable_offices)-1])
            x.rana_f_office=False
            x.thread_count = 256
            x.init_ip_list(ip_list,office_subnet2)
            x.start()     
            
    

            

        return self



