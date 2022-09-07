import subprocess
import threading
import time

def func1(a,b):
    for i in range(10):
        print(f"fonction 1: args=( {a},{b} ) percentage:"+str((i+1)*10)+"%")
        time.sleep(1)

def func2():
    for i in range(10):
        print("fonction 2: percentage:"+str((i+1)*10)+"%")
        time.sleep(1)

def func3(a,b,c):
    for i in range(10):
        print(f"fonction 3: args=( {a},{b},{c} ) percentage:"+str((i+1)*10)+"%")
        time.sleep(1)


def func4(a,b):
    p = subprocess.Popen('ping -n 2 10.10.10.10',stdout = subprocess.DEVNULL)
    p.wait()
    result=(p.poll()==0)
    print (f"fonction : args=( {a},{b} ) result:  "+str(result))
   

def start_threads(function_list,args_list):
    threads = []
    rng=256
    for i in range(rng):
        threads.append(threading.Thread(target=function_list[3], args=[i,i]))
        threads[i].start()
    for i in range(rng):
        threads[i].join()

#MAIN PROGRAM
start_time = time.time()


function_list=[func1,func2,func3,func4]
args_list=[[1,2],[],[4,5,6]]
start_threads(function_list,args_list)

print("--- %s seconds ---" % (time.time() - start_time))
