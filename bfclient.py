__author__ = 'Danny Taing'

import socket
import sys
import datetime

class Node:
    def __init__(self, ip, port, cost, link):
        self.ip = ip
        self.port = port
        self.cost = cost
        self.link = link

    def __init__(self, ip, port, cost):
        self.ip = ip
        self.port = port
        self.cost = cost
        self.link = ""

class DistanceVector:
    def __init__(self, source, neighbors_dict):
        self.source = source
        # Initialize DV table with direct neighbors
        self.dv_dict = neighbors_dict
        for dest, neighbor in self.dv_dict:
            neighbor.link = dest







def main():
    local_ip = "127.0.0.1"
    local_port, timeout, neighbors_list = getArgs()

    # Dictionary to maintain information only about directly attached neighbors
    neighbors_dict = {}
    for i in range(0, len(neighbors_list), 3):
        ip = neighbors_list[i]
        port = neighbors_list[i+1]
        cost = neighbors_list[i+2]
        dest = ip + ":" + port
        temp_neighbor = Node(ip, port, cost)
        neighbors_dict[dest] = temp_neighbor

    # DV table initially contains only routing information about direct neighbors
    localDV = DistanceVector(local_ip + ":" + local_port, neighbors_dict)
    





def getArgs():
    localport = int(sys.argv[1])
    timeout = int(sys.argv[2])
    neighbors_list = []
    for i in range(3, len(sys.argv)):
        neighbors_list.append(sys.argv[i])
    return localport, timeout, neighbors_list

def printDVList(neighbors_dict):
    current_time = datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))
    print "<" + str(current_time) + "> Distance vector list is:"
    for dest, dv in neighbors_dict.iteritems():
        print "Destination = " + dest + ", Cost = " + dv + ", Link = "




main()



