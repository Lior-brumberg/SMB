# -*- coding: utf-8 -*-
from scapy.all import *
import logging

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


def swap_endian(l):
    swapped = []
    for i in range(0, len(l), 2):
        swapped.insert(0, l[i:i+2])

    return ''.join(swapped)


def session_setup(st):
    st = st[SMB_HEADER_BUFFER + SESSION_SETUP_BUFFER:]
    try:
        index = st.index('4e544c4d53535000')
        st = st[index:]

    except ValueError:
        print "Not NTLMSSP"
        return

    domain_lngth = st[DOMAIN_NAME_LENGTH_SETUP_BUFFER:DOMAIN_NAME_LENGTH_SETUP_BUFFER + DOMAIN_NAME_LENGTH_SETUP_LENGTH]
    domain_lngth = swap_endian(domain_lngth)
    domain_lngth = int(domain_lngth, 16)

    domain_offset = st[DOMAIN_NAME_OFFSET_SETUP_BUFFER:DOMAIN_NAME_OFFSET_SETUP_BUFFER+DOMAIN_NAME_OFFSET_SETUP_LENGTH]
    domain_offset = swap_endian(domain_offset, 16)
    domain_offset = int(domain_offset, 16)
    
    domain_name = st[domain_offset:domain_offset + domain_lngth]

    username_lngth = st[DOMAIN_NAME_LENGTH_SETUP_BUFFER:DOMAIN_NAME_LENGTH_SETUP_BUFFER + DOMAIN_NAME_LENGTH_SETUP_LENGTH]
    username_lngth = swap_endian(username_lngth)
    username_lngth = int(username_lngth, 16)

    username_offset = st[DOMAIN_NAME_OFFSET_SETUP_BUFFER:DOMAIN_NAME_OFFSET_SETUP_BUFFER+DOMAIN_NAME_OFFSET_SETUP_LENGTH]
    username_offset = swap_endian(username_offset, 16)
    username_offset = int(username_offset, 16)

    username = st[username_offset:username_offset + username_lngth]

    print "domain name: {0}\nname: {1}".format(domain_name, username)

to_hex = lambda x: "".join((hex(ord(c))[2:].zfill(2) for c in x))


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

    ##getattr(smb_commands, command)(pkt) for later use
    if command == 'session_setup':
        session_setup(hex_s)


def main():
    """
    Add Documentation here
    """
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    sniff(count=0, lfilter=filter_smb, store=0, prn=packet_handler)

if __name__ == '__main__':
    main()
