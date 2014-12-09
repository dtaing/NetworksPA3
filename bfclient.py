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

    def __init__(self, ip, port, cost, is_neighbor):
        self.ip = ip
        self.port = port
        self.cost = cost
        self.link = ""
        self.is_neighbor = is_neighbor

class DistanceVector:
    def __init__(self, source, neighbors_dict):
        self.source = source
        # Initialize DV table with direct neighbors
        self.dv_dict = neighbors_dict
        for dest, neighbor in self.dv_dict.iteritems():
            neighbor.link = dest
            neighbor.is_neighbor = True

    def add_node(self, ip, port, cost, is_neighbor):
        self.dv_dict[ip + ":" + port] = Node(ip, port, cost, is_neighbor)

    def printDVList(self):
        current_time = datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))
        print "<" + str(current_time) + "> Distance vector list is:"
        for dest, dv in self.dv_dict.iteritems():
            if dest != me:
                print "Destination = " + dest + ", Cost = " + str(dv.cost) + ", Link = (" + dv.link + ")"

def getArgs():
    local_port = sys.argv[1]
    timeout = sys.argv[2]
    neighbors_list = []
    for i in range(3, len(sys.argv)):
        neighbors_list.append(sys.argv[i])
    return local_port, timeout, neighbors_list

def setup_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print "listening on {0}:{1}\n".format(host, port)
    return sock

def broadcast_costs():
    """ send estimated path costs to each neighbor """


if __name__ == "__main__":
    local_ip = socket.gethostbyname(socket.gethostname())
    local_port, timeout, neighbors_list = getArgs()

    # Dictionary to maintain information only about directly attached neighbors
    neighbors_dict = {}
    for i in range(0, len(neighbors_list), 3):
        ip = neighbors_list[i]
        port = neighbors_list[i+1]
        cost = neighbors_list[i+2]
        dest = ip + ":" + port
        temp_neighbor = Node(ip, port, cost, True)
        neighbors_dict[dest] = temp_neighbor

    # DV table initially contains only routing information about direct neighbors
    myDV = DistanceVector(local_ip + ":" + local_port, neighbors_dict)

    # Add myself to DV list
    me = local_ip + ":" + local_port
    myDV.add_node(local_ip, local_port, cost=0.0, is_neighbor=False)
    myDV.printDVList()

    # Begin accepting ROUTE UPDATES from neighbors
    sock = setup_server(local_ip, int(local_port))




