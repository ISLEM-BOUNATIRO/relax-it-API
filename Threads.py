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

def start_threads(function_list,args_list):
    threads = []
    for i in range(len(function_list)):
        threads.append(threading.Thread(target=function_list[i], args=args_list[i]))
        threads[i].start()

#MAIN PROGRAM
function_list=[func1,func2,func3]
args_list=[[1,2],[],[4,5,6]]
start_threads(function_list,args_list)

