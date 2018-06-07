# -*- coding: utf-8 -*-
import socket
import subprocess

SERVER_IP = '192.168.2.157'
SERVER_PORT = 5555

def main():
    s = socket.socket()
    s.connect((SERVER_IP, SERVER_PORT))

    s.settimeout(None)
    while True:
        data = s.recv(256)
        if data != "":
            if data.startswith("1"):
                data = data[1:]
                procs = subprocess.check_output(['handle', '\\' + data], shell=True)
                s.send(procs)
            elif data.startswith("2"):
                data = data[1:]
                data = data.split()
                for pid in data:
                    subprocess.call(['taskkill', '/f', '/pid', pid], shell=True)
            
        else:
            s.close()

main()
