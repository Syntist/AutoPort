import psutil
import json
import subprocess
import pythonupnp as upnp
from time import sleep 
from os import system

clear = "cls"

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    check = last_line.split(":")
    if(check[0] != "INFO"):
        # check in last line for process name
        removeSpace = last_line.replace(" ", "")
        pid = removeSpace.split(".exe")
        pid = pid[1].split("C")
        return int(pid[0])
    else:
        return False

def onExit(port):
    for x in ports:
        if(x.status == 'active'):
            upnp.deletePort(x)

def runtimeCheck(ports):
    flag = 0
    for x in ports:
        if(x.status == 'disabled'):
            pid = process_exists(x.appName)
            if(pid): 
                x.pid = pid
                upnp.addPort(x)
                flag = 1
        
        else:
            if(psutil.pid_exists(x.pid) is False):
                upnp.deletePort(x)
                flag = 1
    
    if(flag == 1):
        display(ports)


def display(ports): 
    system(clear)
    for x in ports:
        print(f'{x.appName:25s}{x.port:10s}{x.portType:10s}{x.status:10s}')
    print("Press Ctrl-C To Exit")


# Reading Data From File
f = open("PortData.json", "r")
dataFile = f.read()
arrayPort = json.loads(dataFile)
ports = []

for i in arrayPort:
    portData = upnp.PortInfo(i)
    portData.appName = portData.appName.lower()
    portData.portType = portData.portType.upper()
    ports += [portData]

display(ports)
try:
    while True:
        runtimeCheck(ports)
        sleep(2)
except KeyboardInterrupt:
    pass

onExit(ports)