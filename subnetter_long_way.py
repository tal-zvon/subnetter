#!/usr/bin/env python3

###########
# Imports #
###########

import signal
import sys

##################
# CTRL+C Handler #
##################

def signal_handler(*_):
    print("\nExiting...")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

#############
# Functions #
#############

def parse_ip(raw_ip):
    ip_str_list = raw_ip.split(".")

    if len(ip_str_list) != 4:
        raise ValueError

    # Exceptions will be caught by main program
    ip_int_list = [ int(val) for val in ip_str_list ]

    for val in ip_int_list:
        if val < 0 or val > 255:
            raise ValueError

    return ip_int_list

def parse_subnet_mask(raw_subnet_mask):
    subnet_mask_int_list = parse_ip(raw_subnet_mask)

    for val in subnet_mask_int_list:
        if val not in (0, 128, 192, 224, 240, 248, 252, 254, 255):
            raise ValueError

    allowed_non_zero = True
    for val in subnet_mask_int_list:
        if not allowed_non_zero:
            if val is not 0:
                raise ValueError

        if val is not 255:
            allowed_non_zero = False

    return subnet_mask_int_list

def get_class(ip):
    first_octet = int(ip.split(".")[0])

    bits_set = []
    for i in range(8):
        bits_set.append(first_octet >> i & 1)

    bits_set.reverse()
    
    bit_counter = 0
    for bit in bits_set:
        if bit:
            bit_counter += 1
        else:
            break

    if bit_counter is 0:
        return "A"
    elif bit_counter is 1:
        return "B"
    elif bit_counter is 2:
        return "C"
    elif bit_counter is 3:
        return "D"
    elif bit_counter is 4:
        return "E"

########
# Main #
########

while True:
    raw_ip = input("Enter IP: ")

    try:
        ip = parse_ip(raw_ip)
    except ValueError:
        print("This IP is invalid\n")
        continue

    raw_subnet_mask = input("Enter Subnet Mask: ")

    try:
        subnet_mask = parse_subnet_mask(raw_subnet_mask)
    except ValueError:
        print("This subnet mask is invalid\n")
        continue

    # Network
    network = []
    str_network = []
    for i in range(4):
        network.append(ip[i] & subnet_mask[i])
        str_network.append(str(ip[i] & subnet_mask[i]))

    # First host
    first_host = network[:3]
    first_host.append(network[3] + 1)
    str_first_host = [ str(val) for val in first_host ]

    # Wildcard
    wildcard = [ x ^ 255 for x in subnet_mask ]

    # Broadcast
    broadcast = []
    str_broadcast = []

    for i in range(4):
        broadcast.append(network[i] ^ wildcard[i])
        str_broadcast.append(str(network[i] ^ wildcard[i]))

    # Last host
    last_host = broadcast[:3]
    last_host.append(broadcast[3] - 1)
    str_last_host = [ str(val) for val in last_host ]

    # Output
    print("Network: {}".format('.'.join(str_network)))
    print("First Host: {}".format('.'.join(str_first_host)))
    print("Last Host: {}".format('.'.join(str_last_host)))
    print("Broadcast: {}".format('.'.join(str_broadcast)))
    if get_class(raw_ip):
        print("Class: {}".format(get_class(raw_ip)))

    print()
