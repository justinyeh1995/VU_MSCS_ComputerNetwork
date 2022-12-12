###########################
## Author: Chih-Ting Yeh ##
###########################

import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import zmq    # this package must be imported for ZMQ to work
import subprocess
import re
import pandas as pd
import docker 
import networkx as nx
import json
import csv

'''pseudo=
should be done manually
- ping all nodes in the overlay network: using test_client.py's logic(as shown in the lecture slides)
- get the avg. delay of each entity (ping -c 10 ip | grep rtt | awk ...)

- compute the shortest path with Dijkstra’s algo (done) 
- construct table !! (done) 
- publish it so that each entity in the overlay network know where to go (done)
'''

def build_graph(topo):
  g = nx.Graph()
  for edges in [line.strip().split(",") for line in topo]:
    src, dst, w = edges
    print(edges)
    g.add_edge(src,dst,weight=float(w))
  return g

def shortest_path(src, dst, g, weight=None):
  path = nx.shortest_path(g, source=src, target=dst, weight=weight, method='dijkstra')
  return path

def broadcast(path):
  with open('mapping.json', 'r') as f:
    mapping = json.load(f)
  f.close()

  with open('container2ip.json', 'r') as f:
    containerMapping = json.load(f)
  f.close()
  ConnectIP = ''
  for i in range(len(path)):
    if i < len(path) - 1:
      src, dst = path[i], path[i+1]
      src_ip = mapping[src]
      BindIP = ConnectIP if ConnectIP != '' else containerMapping[dst][src] 
      ConnectIP = containerMapping[src][dst] 
      socks = {"bind": BindIP, "connect": ConnectIP}
      out_file = open("route.json", "w")
      json.dump(socks, out_file, indent = 4)
      print(src)
      print(src_ip)
      out_file.close()
      remote = f'cc@{src_ip}:/home/cc/justin/'
      subprocess.run (['scp', '-i', '~/.ssh/cs4283_5283.pem', 'route.json', remote])
    else:
      route = {"bind": ConnectIP}
      out_file = open("route.json", "w")
      json.dump(route, out_file, indent = 4)
      dst_ip = mapping[dst]
      print(dst)
      print(dst_ip)
      print(ConnectIP)
      out_file.close()
      remote = f'cc@{dst_ip}:/home/cc/justin/'
      subprocess.run (['scp', '-i', '~/.ssh/cs4283_5283.pem', 'route.json', remote])
  
##################################
# Driver program
##################################

def driver ():
  topo = open("topology.csv", newline ='\n')
  g = build_graph (topo)
  topo.close()
  #path = shortest_path ("C", "S", g, weight=None)
  path = shortest_path ("C", "S", g, weight='weight')
  print(path)
  broadcast(path)
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Send Distributed Routing Table")
    
  # start the driver code
  driver()

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  #print("Current libzmq version is %s" % zmq.zmq_version())
  #print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
