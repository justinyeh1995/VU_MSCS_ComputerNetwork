# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom network protocol
#          For assignment 1, this will be very simple and will include
#          all the ZeroMQ logic
#

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")

# import the zeromq capabilities
import zmq
import netifaces as ni
import random


############################################
#  Bunch of Network Layer Exceptions
#
# @TODO@ Add whatever make sense here.
############################################

############################################
#       Custom Network Protocol class
############################################
class CustomNetworkProtocol():
    '''Custom Network Protocol'''

    ###############################
    # constructor
    ###############################
    def __init__(self):
        self.role = None  # indicates if we are client or server, false => client
        self.config = None  # network configuration
        self.ctx = None  # ZMQ context
        self.socket = None  # At this stage we do not know if more than one socket needs to be maintained
        self.poller = None
        self.socket_string = ""
        self.ip2host = {f"10.0.0.{i}": f"H{i}" for i in range(1, 20)}
        self.host2ip = {f"H{i}": f"10.0.0.{i}" for i in range(1, 20)}
        self.host_des_next = []
        self.server_lst = ["H5", "H6"]
        self.router_port = 4444
        self.server_port = 5555

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, config, role, ip, port, routing_table='routingTable.txt'):
        try:
            # Here we initialize any internal variables
            print("Custom Network Protocol Object: Initialize")
            self.config = config
            self.role = role
            # This object is held by Client, but the ip and port is of its destination server
            self.ip = ip
            self.port = port
            self.routing_table = routing_table
            self.conn_socks = {}

            # initialize our variables
            print("Custom Network Protocol Object: Initialize - get ZeroMQ context")
            self.ctx = zmq.Context()
            try:
                with open(self.routing_table, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        words = line.strip().split(" ")
                        self.host_des_next.append([words[0], words[1], words[2]])
            except:
                print("Some exception occurred getting txt {}".format(sys.exc_info()[0]))
                return
            # initialize the config object

            # initialize our ZMQ socket
            #
            # @TODO@
            # DEALER-ROUTER pair supports asynchronous transport.
            if (self.role):
                # we are the server side
                print("Custom Network Protocol Object: Initialize - get ROUTER socket")
                self.socket = self.ctx.socket(zmq.REP)
                # since we are server, we bind
                bind_str = "tcp://" + self.ip + ":" + str(self.port)
                print("Custom Network Protocol Object: Initialize - server binds socket to {}".format(bind_str))
                self.socket.bind(bind_str)
                self.socket_string = bind_str
            else:
                # we are the client side
                print("Custom Network Protocol Object: Initialize - get DEALER socket")
                self.socket = self.ctx.socket(zmq.DEALER)
                self.poller = zmq.Poller()
                self.poller.register(self.socket, zmq.POLLIN)
                try:
                    # set our identity
                    final_addr = self.ip + ":" + str(self.port)
                    print("client setting its identity: {}".format(final_addr))
                    self.socket.setsockopt(zmq.IDENTITY, bytes(final_addr, "utf-8"))
                except zmq.ZMQError as err:
                    print("ZeroMQ Error setting sockopt: {}".format(err))
                    return
                except:
                    print("Some exception occurred setting sockopt on REQ socket {}".format(sys.exc_info()[0]))
                    return
                # since we are client, we connect
                try:
                    print("Looking up the Routing Table...")
                    my_ip = "127.0.0.1"
                    intfs = ni.interfaces()
                    for intf in intfs:
                        if 'eth0' in intf:
                            my_ip = ni.ifaddresses(intf)[ni.AF_INET][0]['addr']
                    print("IP Address of this host is " + my_ip)
                    final_dst = self.ip
                    print("Final destination of this packet is " + final_dst)
                    for entry in self.host_des_next:
                        print(entry[0] + ":" + entry[1] + ":" + entry[2])
                        if entry[0] == self.ip2host[my_ip] and entry[1] == final_dst:
                            nexthophost = entry[2]
                    nexthopaddr = self.host2ip[nexthophost]
                    connect_string = "tcp://" + nexthopaddr + ":" + str(4444)
                    print("Custom Network Protocol Object: Initialize - client connects socket to {}".format(
                        connect_string))
                    self.socket.connect(connect_string)
                    self.socket_string = connect_string
                except zmq.ZMQError as err:
                    print("ZeroMQ Error connecting REQ socket: {}".format(err))
                    self.socket.close()
                    return
                except:
                    print("Some exception occurred connecting REQ socket {}".format(sys.exc_info()[0]))
                    self.socket.close()
                    return
            # since we are client, we connect
            # connect_str = "tcp://" + self.ip + ":" + str(self.port)
            # print("Custom Network Protocol Object: Initialize - connect socket to {}".format(connect_str))
            # self.socket.connect(connect_str)
        except Exception as e:
            raise e  # just propagate it

    ##################################
    # Driver program
    ##################################
    def initialize_router(self, config, myaddr, myport, routing_table='routingTable.txt'):
        ''' Initialize the object '''
        # Here we initialize any internal variables
        print("Custom Network Protocol Object: Initialize")
        self.config = config
        # self.role = role
        self.myaddr = myaddr
        self.myport = myport
        self.host_des_next = []
        self.routing_table = routing_table
        self.conn_socks = {}
        # initialize the routing table
        try:
            with open(self.routing_table, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    words = line.strip().split(" ")
                    self.host_des_next.append([words[0], words[1], words[2]])
        except:
            print("Some exception occurred getting txt {}".format(sys.exc_info()[0]))
            return

        # initialize the config object
        # @TODO@

        # initialize our ZMQ socket
        #
        # @TODO@

        try:
            # every ZMQ session requires a context
            print("Obtain the ZMQ context")
            context = zmq.Context()  # returns a singleton object
            print("Obtain the Poller")
            poller = zmq.Poller()
            # The socket concept in ZMQ is far more advanced than the traditional socket in
            # networking. Each socket we obtain from the context object must be of a certain
            # type. For TCP, we will use ROUTER for server side (many other pairs are supported
            # in ZMQ for tcp.
            print("Obtain the ROUTER type socket")
            bind_sock = context.socket(zmq.ROUTER)
        except zmq.ZMQError as err:
            print("ZeroMQ Error obtaining context/Poller/ROUTER: {}".format(err))
            return
        except:
            print("Some exception occurred getting context/Poller/ROUTER {}".format(sys.exc_info()[0]))
            return

        try:
            # as in a traditional socket, tell the system what port are we going to listen on
            # Moreover, tell it which protocol we are going to use, and which network
            # interface we are going to listen for incoming requests. This is TCP.
            print("Bind the ROUTER socket")
            bind_string = "tcp://" + myaddr + ":" + str(myport)
            print("TCP router will be binding on {}".format(bind_string))
            bind_sock.bind(bind_string)
        except zmq.ZMQError as err:
            print("ZeroMQ Error binding ROUTER socket: {}".format(err))
            bind_sock.close()
            return
        except:
            print("Some exception occurred binding ROUTER socket {}".format(sys.exc_info()[0]))
            bind_sock.close()
            return

        try:
            # register sockets
            print("Register sockets for incoming events")
            poller.register(bind_sock, zmq.POLLIN)
            # poller.register(conn_sock, zmq.POLLIN)
        except zmq.ZMQError as err:
            print("ZeroMQ Error registering with poller: {}".format(err))
            return
        except:
            print("Some exception occurred getting poller {}".format(sys.exc_info()[0]))
            return

        # since we are a server, we service incoming clients forever
        print("Router now starting its forwarding loop")
        while True:
            # collect all the sockets that are enabled in this iteration
            socks = dict(poller.poll())
            # Now handle the event for each enabled socket
            if bind_sock in socks:
                # we are here implies that the bind_sock had some info show up.
                try:
                    #  Wait for next request from previous hop. When using DEALER/ROUTER, it is suggested to use
                    # multipart send/receive. What we receive will comprise the sender's info which we must preserve, an empty
                    # byte, and then the actual payload
                    print("Receive from prev hop")
                    request = bind_sock.recv_multipart()
                    print("Router received request from prev hop via ROUTER: %s" % request)
                    final_dst_pos = -3
                    if len(request) < 3:
                        final_dst_pos = -2
                    final_dst = request[final_dst_pos].decode("utf-8").split(":")[0]
                    ###################
                    ## Table Look Up ##
                    ###################
                    print("Looking up the Routing Table...")
                    my_ip = "127.0.0.1"
                    intfs = ni.interfaces()
                    for intf in intfs:
                        if 'eth0' in intf:
                            my_ip = ni.ifaddresses(intf)[ni.AF_INET][0]['addr']
                    print("IP Address of this host is " + my_ip)
                    print("Final destination of this packet is " + final_dst)
                    # already connected
                    if final_dst in self.conn_socks:
                        conn_sock = self.conn_socks[final_dst]
                    else:
                        for entry in self.host_des_next:
                            if entry[0] == self.ip2host[my_ip] and entry[1] == final_dst:
                                nexthophost = entry[2]
                        nexthopaddr = self.host2ip[nexthophost]
                        print("Router acquiring connection socket")
                        conn_sock = context.socket(zmq.DEALER)
                        print("router setting its identity: {}".format(self.ip2host[my_ip]))
                        conn_sock.setsockopt(zmq.IDENTITY, bytes(self.ip2host[my_ip], "utf-8"))
                        print("Router connecting to next hop")
                        nexthopport = self.router_port
                        # sever port adjustment here
                        if nexthophost in self.server_lst:
                            nexthopport = self.server_port
                        connect_string = "tcp://" + nexthopaddr + ":" + str(nexthopport)
                        print("TCP router will be connecting to {}".format(connect_string))
                        conn_sock.connect(connect_string)
                        print("Register sockets: " + connect_string + " for incoming events")
                        poller.register(conn_sock, zmq.POLLIN)
                        print("Now the number of sockets is " + str(len(poller.sockets)))
                        self.conn_socks[final_dst] = conn_sock
                    print("Router send packet to next hop via DEALER")
                    conn_sock.send_multipart(request)
                except zmq.ZMQError as err:
                    print("ZeroMQ Error receiving/setting sockopt/ getting DEALER socket: {}".format(err))
                    bind_sock.close()
                    return
                except:
                    print("Some exception occurred receiving/sending {}".format(sys.exc_info()[0]))
                    bind_sock.close()
                    return

            for conn_sock in self.conn_socks.values():
                print("Checking the DEALERs...")
                if conn_sock in socks:
                    try:
                        #  Wait for response from next hop
                        response = conn_sock.recv_multipart()
                        print("Router received response from next hop via DEALER: %s" % response)
                    except zmq.ZMQError as err:
                        print("ZeroMQ Error receiving response: {}".format(err))
                        conn_sock.close()
                        return
                    except:
                        print("Some exception occurred receiving response {}".format(sys.exc_info()[0]))
                        conn_sock.close()
                        return

                    try:
                        #  Send reply back to previous hop. request[0] is the original client identity preserved at every hop
                        # response[1] has actual payload
                        print("Send reply to prev hop via ROUTER")
                        bind_sock.send_multipart(response)
                    except zmq.ZMQError as err:
                        print("ZeroMQ Error sending: {}".format(err))
                        bind_sock.close()
                        return
                    except:
                        print("Some exception occurred receiving/sending {}".format(sys.exc_info()[0]))
                        bind_sock.close()
                        return



    ##################################
    #  send network packet, final state: sent
    ##################################
    def send_packet(self, packet, size, stable=False):
        try:
            # Here, we simply delegate to our ZMQ socket to send the info
            print("Custom Network Protocol::send_packet")
            # @TODO@ - this may need mod depending on json or serialized packet
            # self.socket.send (bytes(packet, "utf-8"))
            #  @TODO using random number logic, either (a) send the chunk to the next hop, or (b) delay it, or (c) just don’t send it at all and drop it.
            if self.role or stable:
                print("Send packet successfully to socket " + self.socket_string)
                self.socket.send_multipart([b'', packet])
            else:
                strategy = random.randint(1, 2)
                if strategy == 1:
                    print("Send packet successfully to socket " + self.socket_string)
                    print(packet)
                    self.socket.send_multipart([b'', packet])
                elif strategy == 2:
                    print("Send packet unsuccessfully to socket " + self.socket_string)
        except Exception as e:
            raise e

    ######################################
    #  receive network packet, final state: recv
    ######################################
    def recv_packet(self, packet_size=1024):
        try:
            print("Custom Network Protocol::recv_packet")
            # @TODO@ Note that this method always receives bytes. So if you want to
            # convert to json, some mods will be needed here. Use the config.ini file.
            # self.socket.send (bytes(packet, "utf-8"))
            print("Trying to receive from socket " + self.socket_string)
            multi_part = self.socket.recv_multipart()
            print("Received: " + str(len(multi_part)))
            packet = multi_part[-1]
            print("packet is " + str(packet))
            # cur_len = len(packet)
            # while cur_len < packet_size:
            #    packet = packet + self.socket.recv()
            print("Receive from socket!")
            return packet
        except Exception as e:
            raise e

    def get_socket(self):
        return self.socket

    def get_poller(self):
        return self.poller
