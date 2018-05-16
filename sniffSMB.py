# -*- coding: utf-8 -*-
from scapy.all import *
import smb_commands

COMMAND_BUFFER = 20
COMMAND_SIZE = 2
FLAGS_BUFFER = 24
FLAGS_SIZE = 4
NEXT_COMMAND_BUFFER = 28
NEXT_COMMAND_SIZE = 4
ASYNC_FLAG_BUFFER = 1

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


def get_hex_string(s):
    to_hex = lambda x: "".join((hex(ord(c))[2:].zfill(2) for c in x))
    hex_s = to_hex(s)
    return hex_s


def filter_smb(pkt):
    """
    Filters received packets, only SMB packets can pass this selection
    """
    try:
        raw_string = pkt[Raw]
        hex_s = get_hex_string(raw_string)
        return hex_s.startswith('fe534d42')

    except IndexError:
        return False


def packet_handler(pkt):
    raw_string = pkt[Raw]
    hex_s = get_hex_string(raw_string)
    command = hex_s[COMMAND_BUFFER:COMMAND_BUFFER + COMMAND_SIZE]

    flags = hex_s[FLAGS_BUFFER:FLAGS_BUFFER + FLAGS_SIZE]
    if flags[ASYNC_FLAG_BUFFER] == '1':
        print 'Cannot deal with async SMB!'
        return

    next_command = hex_s[NEXT_COMMAND_BUFFER:NEXT_COMMAND_BUFFER + NEXT_COMMAND_SIZE]
    if next_command != '00000000':
        print 'Cannot deal with compound command!'
        return

    getattr(smb_commands, command)()


def main():
    """
    Add Documentation here
    """
    sniff(count=0, lfilter=filter_smb, store=0, prn=packet_handler)

if __name__ == '__main__':
    main()