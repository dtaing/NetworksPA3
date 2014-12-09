__author__ = 'Danny Taing'

import socket
import sys
import datetime

class DV:
    """A class to represent a client neighbor in distance vector list"""
    def __init__(self, ip_address, port, cost):
        self.ip = ip_address
        self.port = port
        self.cost = cost
        self.dest = ip_address + ":" + port


def main():
    localport, timeout, neighbors_list = getArgs()
    print localport
    print timeout
    print neighbors_list
    dv_dict = {}
    for i in range(0, len(neighbors_list), 3):
        ip = neighbors_list[i]
        port = neighbors_list[i+1]
        cost = neighbors_list[i+2]
        temp_neighbor = DV(ip, port, cost)
        dest = temp_neighbor.dest
        dv_dict[dest] = temp_neighbor

    printDVList(dv_dict)


def getArgs():
    localport = int(sys.argv[1])
    timeout = int(sys.argv[2])
    neighbors_list = []
    for i in range(3, len(sys.argv)):
        neighbors_list.append(sys.argv[i])
    return localport, timeout, neighbors_list

def printDVList(dv_dict):
    current_time = datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))
    print "<" + str(current_time) + "> Distance vector list is:"
    for dest, dv in dv_dict.iteritems():
        print "Destination = " + dest + ", Cost = " + dv.cost + ", Link = "




main()



