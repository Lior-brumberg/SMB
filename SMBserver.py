# -*- coding: utf-8 -*-
import socket
import select
import thread

DATA_BYTES = 64
PORT = 5555
CLIENT_SOCKETS = {}
server_socket = socket.socket()

def init_server():
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    

def listen_to_sockets(drive):
    init_processes = ''
    while True:
        rlist, wlist, xlist = select.selcet([server_socket], [], [])
        for sock in rlist:
            (new_socket, address) = server_socket.accept()
            init_processes = get_processes(address, drive)
            CLIENT_SOCKETS[address] = (new_socket, init_processes)
            
            
        if len(rlist) == 5:
            break

def get_processes(address, drive):
    client_socket = CLIENT_SOCKETS[address][0]
    client_socket.send("1" + drive)
    data = client_socket.recv(4096)
    
    return data


def get_new_process(address, drive):
    #all_processes = get_processes(address, drive)
    #Need to add option to close only new processes
    init_processes = CLIENT_SOCKETS[address][1]

    pid = 0
    list_of_pids = []
    while 'pid:' in init_processes:
        i = init_processes.index('pid:')
        init_processes = init_processes[i + 5:]
        pid = init_processes[:init_processes.index(' ')]
        list_of_pids.append(pid)

    return " ".join(list_of_pids)


def close_processes(address, pids)
    client_socket = CLIENT_SOCKETS[address][0]
    client_socket.send("2" + pids)
    

def close_all_sockets():
    for sock in CLIENT_SOCKETS.values()[0]:
        sock.send("")
        sock.close()

    server_socket.close()

            

        
