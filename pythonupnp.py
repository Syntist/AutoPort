import socket
from os import system
import fnmatch


upnpLocation = ".\\miniupnpc\\upnpc-shared.exe"
log = ">> log.txt"

def start():
    bashCommand = f"{upnpLocation} -l > .\\miniupnpc\\upnpData.txt"
    system(bashCommand)
    upnpData = open(".\\miniupnpc\\upnpData.txt","r")
    for i in upnpData:
        if(fnmatch.fnmatch(i, " desc:*")):
            upnp = i.split(" desc:")
            upnp = upnp[1].split("\n")
            break
    
    return upnp[0]

def getLocalip():
    hostname = socket.gethostname()    
    return socket.gethostbyname(hostname) 

def addPort(portData):
    if(portData.portType == "ALL"):
        bashCommand = f"{upnpLocation} -u {upnpInfo} -a {IPAddr} {portData.port} {portData.port} tcp {log}"
        system(bashCommand)
        bashCommand = f"{upnpLocation} -u {upnpInfo} -a {IPAddr} {portData.port} {portData.port} udp {log}"
        system(bashCommand)
    else:
        bashCommand = f"{upnpLocation} -u {upnpInfo} -a {IPAddr} {portData.port} {portData.port} {portData.portType} {log}"
        system(bashCommand)
        print("bashCommand")
    portData.status = "active"
    
def deletePort(portData):
    if(portData.portType == "ALL"):
        bashCommand = f"{upnpLocation} -u {upnpInfo} -d {portData.port} tcp 0 {log}"
        system(bashCommand)
        bashCommand = f"{upnpLocation} -u {upnpInfo} -d {portData.port} udp 0 {log}"
        system(bashCommand)
    else:
        bashCommand = f"{upnpLocation} -u {upnpInfo} -d {portData.port} {portData.portType} 0 {log}"
        system(bashCommand)
    portData.status = "disabled"

def pause():
    programPause = input("Press the <ENTER> key to continue...")

class PortInfo:
    appName = ''
    port = None
    portType = ''
    status = 'disabled'
    pid = ''

    def __init__(self, args):
        self.appName = args['name']
        self.port = args['port']
        self.portType = args['type']

IPAddr = getLocalip()
upnpInfo = start()