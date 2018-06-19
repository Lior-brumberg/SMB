# -*- coding: utf-8 -*-
from scapy.all import *
from database import Database
import unicodedata


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

CREATE_FLAGS_BUFFER = 24
CREATE_FLAGS_SIZE = 4

READ_FLAG_INDEX = -1
WRITE_FLAG_INDEX = -2
DELETE_FLAG_INDEX = -17

to_hex = lambda x: "".join((hex(ord(c))[2:].zfill(2) for c in x))


def get_authorization(ip):
    db = Database("FAKE_DRIVB_DB")
    data = db.Display_all('Users')
    for row in data:
        if ip == row[0].encode('utf-8'):
            return row[1]
    print ip + "isn\'t in database. Inserting to database..."
    db.insert_data("Users", "IP, Authorization", "\'" + ip + "\', \'" + "-1" + "\'")
    return '-1'


def swap_endian(l):
    swapped = []
    for i in range(0, len(l), 2):
        swapped.insert(0, l[i:i+2])

    return ''.join(swapped)


def create(pkt):
    ipsrc = pkt[IP].src
    auth = get_authorization(ipsrc)
    raw_string = str(pkt[Raw])
    hex_s = to_hex(raw_string)
    hex_s = swap_endian(hex_s)
    bin_s = bin(int(hex_s, 16))[2:].zfill(4 * len(hex_s))
    if auth == 3:
        return False
    else:
        if bin_s[DELETE_FLAG_INDEX]:
            return ipsrc

        elif bin_s[WRITE_FLAG_INDEX]:
            if auth < 2:
                return ipsrc
            else:
                return False
            
        elif bin_s[READ_FLAG_INDEX]:
            if auth < 1:
                return ipsrc
            else:
                return False
    

def read(pkt):
    ipsrc = pkt[IP].src
    auth = get_authorization(ipsrc)
    if auth < 1:
        return ipsrc
    else:
        return False


def write(pkt):
    ipsrc = pkt[IP].src
    auth = get_authorization(ipsrc)
    if auth < 2:
        return ipsrc
    else:
        return False


def session_setup(pkt):
    raw_string = str(pkt[Raw])
    st = to_hex(raw_string)
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

    print "domain name: {0}\tname: {1}\nHas logged in.".format(domain_name, username)
    return None
