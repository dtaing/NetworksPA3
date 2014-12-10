__author__ = 'Danny Taing'

import socket
import sys
import datetime
import select
import json
import threading
import time
import copy

BUFFER = 2048

class Node:
    def __init__(self, ip, port, cost, link):
        self.ip = ip
        self.port = port
        self.cost = cost
        self.link = link
        self.routingtable = {}

    def __init__(self, ip, port, cost, is_neighbor):
        self.ip = ip
        self.port = port
        self.cost = cost
        self.link = ""
        self.is_neighbor = is_neighbor
        self.routingtable = {}

class DistanceVector:
    def __init__(self, source, neighbors_dict):
        self.source = source
        # Initialize DV table with direct neighbors
        self.dv_dict = copy.deepcopy(neighbors_dict)
        for dest, neighbor in self.dv_dict.iteritems():
            neighbor.link = dest
            neighbor.is_neighbor = True

    def add_node(self, ip, port, cost, is_neighbor):
        self.dv_dict[ip + ":" + port] = Node(ip, port, cost, is_neighbor)

    def printDVList(self):
        current_time = datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))
        print "<" + str(current_time) + "> Distance vector list is:"
        for dest, node in self.dv_dict.iteritems():
            if dest != me:
                print "Destination = " + dest + ", Cost = " + str(node.cost) + ", Link = (" + node.link + ")"

class RepeatTimer(threading.Thread):
    def __init__(self, interval, target):
        threading.Thread.__init__(self)
        self.target = target
        self.interval = interval
        self.daemon = True
        self.stopped = False
    def run(self):
        while not self.stopped:
            time.sleep(self.interval)
            self.target()


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

def estimate_costs():
    """ Use Bellman-Ford Algorithm to recalculate distance costs """
    for dest_addr, node in myDV.dv_dict.iteritems():
        # Doesn't matter if it is myself
        if dest_addr != me:
            cost = float("inf")
            nexthop = ""
            for neighbor_addr, neighbor in neighbors_dict.iteritems():
                if dest_addr in neighbor.routingtable:
                    dist = float(neighbor.cost) + float(neighbor.routingtable[dest_addr])
                    if dist < cost:
                        cost = dist
                        nexthop = neighbor_addr
            node.cost = cost
            node.link = nexthop


def broadcast_costs():
    """ Send estimated path costs to each neighbor """
    data = { dest: node.cost for dest, node in myDV.dv_dict.iteritems()}
    for neighbor_dest, neighbor in neighbors_dict.iteritems():
        sock.sendto(json.dumps(data), key_to_addr(neighbor_dest))

def update_costs(host, port, routingtable):
    """ update neighbors' routing tables """
    addr = addr_to_key(host, port)
    # If a node in routingtable is not in our Distance Vector dict, then add it
    for node in routingtable:
        if node not in myDV.dv_dict:
            new_node_ip, new_node_port = key_to_addr(node)
            # new node is not a neighbor as we would know them already so cost is infinite
            myDV.add_node(new_node_ip, str(new_node_port), cost=float("inf"), is_neighbor=False)

    # Copies the received neighbor's routing table to our neighbor node's RT on file
    myDV.dv_dict[addr].routingtable = routingtable
    neighbors_dict[addr].routingtable = routingtable
    # Run Bellman-Ford
    estimate_costs()


def key_to_addr(key):
    ip, port = key.split(":")
    return ip, int(port)

def addr_to_key(ip, port):
    key = ip + ":" + str(port)
    return key

def handle(input):
    input = input.split()
    command = input[0]

    if command == "SHOWRT":
        showrt()

    if command == "LINKDOWN":
        x = 5

    if command == "LINKUP":
        x = 5

    if command == "CLOSE":
        x = 5
    else:
        pass

def showrt():
    myDV.printDVList()




if __name__ == "__main__":
    local_ip = socket.gethostbyname(socket.gethostname())
    local_port, timeout, neighbors_list = getArgs()

    # Dictionary to maintain information only about directly attached neighbors
    neighbors_dict = {}
    for i in range(0, len(neighbors_list), 3):
        ip = neighbors_list[i]
        port = neighbors_list[i+1]
        cost = neighbors_list[i+2]
        dest = addr_to_key(ip, port)
        temp_neighbor = Node(ip, port, cost, True)
        neighbors_dict[dest] = temp_neighbor

    # DV table initially contains only routing information about direct neighbors
    myDV = DistanceVector(addr_to_key(local_ip, local_port), neighbors_dict)

    # Add myself to DV list
    me = local_ip + ":" + local_port
    myDV.add_node(local_ip, local_port, cost=0.0, is_neighbor=False)
    myDV.printDVList()

    # Begin accepting ROUTE UPDATES from neighbors
    sock = setup_server(local_ip, int(local_port))

    broadcast_costs()
    RepeatTimer(int(timeout), broadcast_costs).start()

    # Wait for updates from neighbors and user input
    inputs = [sock, sys.stdin]
    while 1:
        readable, writable, exceptional = select.select(inputs, [], [])
        for s in readable:
            if s == sys.stdin:
                # User input
                user_input = sys.stdin.readline()
                handle(user_input)
            else:
                # Update from neighbor
                data, sender = s.recvfrom(BUFFER)
                print sender
                loaded = json.loads(data)
                update_costs(sender[0], sender[1], loaded)

