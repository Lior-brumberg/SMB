# -*- coding: utf-8 -*-
from scapy.all import *
import logging
import smb_commands
import subprocess
import sys
import getopt
import os

COMMAND_BUFFER = 12
COMMAND_SIZE = 2

FLAGS_BUFFER = 16
FLAGS_SIZE = 4

NEXT_COMMAND_BUFFER = 20
NEXT_COMMAND_SIZE = 4

ASYNC_FLAG_BUFFER = 1

SMB_HEADER_BUFFER = 64
SESSION_SETUP_BUFFER = 24

DOMAIN_NAME_LENGTH_SETUP_BUFFER = 28
DOMAIN_NAME_LENGTH_SETUP_LENGTH = 4
DOMAIN_NAME_OFFSET_SETUP_BUFFER = 36
DOMAIN_NAME_OFFSET_SETUP_LENGTH = 8

USERNAME_LENGTH_SETUP_BUFFER = 44
USERNAME_LENGTH_SETUP_LENGTH = 4
USERNAME_OFFSET_SETUP_BUFFER = 52
USERNAME_OFFSET_SETUP_LENGTH = 8

COMMANDS_DICT = {
    '0000': 'negotiate',
    '0001': 'session_setup',
    '0002': 'logoff',
    '0003': 'tree_connect',
    '0004': 'tree_disconnect',
    '0005': 'create',
    '0006': 'close',
    '0007': 'flush',
    '0008': 'read',
    '0009': 'write',
    '000a': 'lock',
    '000b': 'ioctl',
    '000c': 'cancel',
    '000d': 'echo',
    '000e': 'query_directory',
    '000f': 'change_notify',
    '0010': 'query_info',
    '0011': 'set_info',
    '0012': 'oplock_break',
}


to_hex = lambda x: "".join((hex(ord(c))[2:].zfill(2) for c in x))
get_initial_processes = lambda x: subprocess.check_output(['handle', x])


def filter_smb(pkt):
    """
    Filters received packets, only SMB packets can pass this selection
    """
    try:
        raw_string = str(pkt[Raw])
        hex_s = to_hex(raw_string)
        return hex_s.startswith('fe534d42')

    except IndexError:
        return False


def packet_handler(pkt):
    raw_string = str(pkt[Raw])
    hex_s = to_hex(raw_string)
    command = hex_s[COMMAND_BUFFER:COMMAND_BUFFER + COMMAND_SIZE]
    command = COMMANDS_DICT[command]
    logging.debug(command)
    
    flags = hex_s[FLAGS_BUFFER:FLAGS_BUFFER + FLAGS_SIZE]
    if flags[ASYNC_FLAG_BUFFER] == '1':
        print 'Cannot deal with async SMB!'
        return

    next_command = hex_s[NEXT_COMMAND_BUFFER:NEXT_COMMAND_BUFFER + NEXT_COMMAND_SIZE]
    if next_command != '00000000':
        print 'Cannot deal with compound command!'
        return

    args = [pkt]
    getattr(smb_commands, command)(*args)


def main(argv):
    """
    Add Documentation here
    """
    dir_path = ''
    try:
        opts, arguments = getopt.getopt(argv, "hp:")
    except getopt.GetoptError:
        print 'Usage: sniffSMB.py -p <shared_dir_path>'
        sys.exit(2)

    if not opts:
        print 'Usage: sniffSMB.py -p <shared_dir_path>'
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: sniffSMB.py -p <shared_dir_path>'
            sys.exit()
        elif opt == '-p':
            dir_path = arg
            if not os.path.exists(dir_path):
                print 'No such directory found.'
                sys.exit()
            elif dir_path.startswith('C:'):
                print 'Not a shared directory.'
                sys.exit()


    initial_processes = get_initial_processes(dir_path)
    print initial_processes
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    #sniff(count=0, lfilter=filter_smb, store=0, prn=packet_handler)

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: sniffSMB.py -p <shared_dir_path>"
        sys.exit()
    main(sys.argv[1:])


#fn = 'c:\\file.txt'
#p = os.popen('attrib +h ' + fn)
#t = p.read()
#p.close()