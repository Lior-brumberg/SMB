# -*- coding: utf-8 -*-
import logging
with open('smb.log', 'w'):
    pass
logging.basicConfig(filename='smb.log', level=logging.DEBUG)


from scapy.all import *
import smb_commands
import subprocess
import sys
import getopt
import os
import SMBserver
import thread

USAGE = 'USAGE: sniffSMB.py -p <shared_dir_letter>'

COMMAND_BUFFER = 12 * 2
COMMAND_SIZE = 2 * 2

FLAGS_BUFFER = 16 * 2
FLAGS_SIZE = 4 * 2

NEXT_COMMAND_BUFFER = 20 * 2
NEXT_COMMAND_SIZE = 4 * 2

ASYNC_FLAG_BUFFER = 1 * 2

SMB_HEADER_BUFFER = 64 * 2
SESSION_SETUP_BUFFER = 24 * 2

DOMAIN_NAME_LENGTH_SETUP_BUFFER = 28 * 2
DOMAIN_NAME_LENGTH_SETUP_LENGTH = 4 * 2
DOMAIN_NAME_OFFSET_SETUP_BUFFER = 36 * 2
DOMAIN_NAME_OFFSET_SETUP_LENGTH = 8 * 2

USERNAME_LENGTH_SETUP_BUFFER = 44 * 2
USERNAME_LENGTH_SETUP_LENGTH = 4 * 2
USERNAME_OFFSET_SETUP_BUFFER = 52 * 2
USERNAME_OFFSET_SETUP_LENGTH = 8 * 2

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


def swap_endian(l):
    swapped = []
    for i in range(0, len(l), 2):
        swapped.insert(0, l[i:i+2])

    return ''.join(swapped)


def get_server_from_letter(letter):
    output = subprocess.check_output(['net', 'use'], shell=True)
    output = ''.join(output.split())
    st = output.index(letter)
    output = output[st+4:]
    end = output.index('\\')
    server = output[:end]
    logging.debug("Server found: " + server)
    return server


def filter_smb(pkt):
    """
    Filters received packets, only SMB packets can pass this selection
    """
    try:
        raw_string = str(pkt[Raw])
        hex_s = to_hex(raw_string)
        return 'fe534d42' in hex_s

    except IndexError:
        return False


def wrapper(server):
    def packet_handler(pkt):
        raw_string = str(pkt[Raw])
        hex_s = to_hex(raw_string)
        hex_s = hex_s[hex_s.index('fe534d42'):]
        logging.debug('SMB Packet: ' + hex_s)
        command = hex_s[COMMAND_BUFFER:COMMAND_BUFFER + COMMAND_SIZE]
        command = swap_endian(command)
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
        logging.debug("Command is: " + command)
        try:
            toClose = getattr(smb_commands, command)(*args)
            if toClose:
                logging.debug("{0} Has tried to commit {1}.".format(toClose, command))
                pids = SMBserver.get_new_process(toClose, server)
                SMBserver.close_processes(toClose, pids)
                
        except AttributeError:
            print 'We do not support {0} command yet'.format(command)

    return packet_handler


def check_input(args):
    dir_letter = ''

    try:
        opts, arguments = getopt.getopt(args, "hp:")
    except getopt.GetoptError:
        print USAGE
        sys.exit(2)

    if not opts:
        print USAGE
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print USAGE
            sys.exit()
        elif opt == '-p':
            dir_letter = arg
            logging.debug("Network Drive prompted: " + dir_letter)
            if ':' not in dir_letter:
                dir_letter += ':'

            if not os.path.exists(dir_letter):
                print 'No such directory found.'
                logging.debug("No network drive {}".format(dir_letter))
                sys.exit()
            elif dir_letter.startswith('C:'):
                print 'Not a shared directory.'
                logging.debug("C: is not a network drive")
                sys.exit()

    return dir_letter


def main(argv):
    """
    Add Documentation here
    """
    logging.debug("Starting...")
    subprocess.call(['secedit', '/configure', '/db'])
    server = get_server_from_letter(check_input(argv))
    SMBserver.init_server()
    thread.start_new_thread(SMBserver.listen_to_sockets, (server, 2))
    sniff(count=0, lfilter=filter_smb, store=0, prn=wrapper(server))

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print USAGE
        sys.exit()
    main(sys.argv[1:])


#fn = 'c:\\file.txt'
#p = os.popen('attrib +h ' + fn)
#p.close()
