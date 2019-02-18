#!/usr/bin/env python3

###########
# Imports #
###########

from ipaddress import IPv4Address, IPv4Network, AddressValueError, NetmaskValueError
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

def get_class(ip):
    first_octet = int(str(ip).split(".")[0])

    bits_set = []
    for i in range(8):
        bits_set.append(first_octet >> i & 1)

    bits_set.reverse()
    
    bit_counter = 0
    for bit in bits_set[:4]:
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
    try:
        ip = IPv4Address(input("Enter IP: "))
    except AddressValueError:
        print("This IP is invalid\n")
        continue

    try:
        network = IPv4Network(str(ip) + "/" + input("Enter Subnet Mask: "), strict=False)
    except NetmaskValueError:
        print("This subnet mask is invalid\n")
        continue

    print("Network: {}".format(network[0]))
    print("First Host: {}".format(network[1]))
    print("Last Host: {}".format(network[-2]))
    print("Broadcast: {}".format(network[-1]))
    print("Class: {}".format(get_class(ip)))

    print()
