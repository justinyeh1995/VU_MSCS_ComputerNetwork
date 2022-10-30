# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom transport protocol
#          For assignment 1, this will be a No-Op. But we keep the layered
#          architecture in all the assignments
#

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")
import time
from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


############################################
#  Bunch of Transport Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################

############################################
#       Custom Transport Protocol class
############################################
class CustomTransportProtocol():
    '''Custom Transport Protocol'''

    ###############################
    # constructor
    ###############################
    def __init__(self, role):
        self.role = role  # indicates if we are client or server, false => client
        self.ip = None
        self.port = None
        self.nw_obj = None  # handle to our underlying network layer object
        self.mtu_len = 16  # maximum segment size
        self.packet_size = 1024
        self.digit_of_original_packet = 4
        self.chunk_num = self.packet_size / self.mtu_len

        self.seq_num = 0

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, config, ip, port):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Custom Transport Protocol Object: Initialize")

            # initialize our variables
            self.ip = ip
            self.port = port

            # in a subsequent assignment, we will use the max segment size for our
            # transport protocol. This will be passed in the config.ini file.
            # Right now we do not care.

            # Now obtain our network layer object
            print("Custom Transport Protocol::initialize - obtain network object")
            self.nw_obj = NWProtoObj()

            # initialize it
            #
            # In this assignment, we let network layer (which holds all the ZMQ logic) to
            # directly talk to the remote peer. In future assignments, this will be the
            # next hop router to whom we talk to.
            print("Custom Transport Protocol::initialize - initialize network object")
            self.nw_obj.initialize(config, self.role, self.ip, self.port)

        except Exception as e:
            raise e  # just propagate it

    ##################################
    #  send application message
    ##################################
    def send_appln_msg(self, payload, size, normal=True):
        try:
            # @TODO@ Implement this
            # Get a serialized message from the app layer along with the payload size.
            # Break the total message into chunks of segment size and send segment by segment depending on the maximum segment size allowed by our transport.
            print("Custom Transport Protocol::send_appln_msg")
            # server side
            if normal:
                self.send_segment(payload)
            # client side
            else:
                size_str = (self.digit_of_original_packet - len(str(size))) * '0' + str(size)
                actual_packet = bytes(size_str, 'utf-8') + payload
                actual_packet += bytes(str('0' * (self.packet_size - len(actual_packet))), 'utf-8')
                # actual_packet = size_str + original_packet + padding zero
                for i in range(0, int(self.chunk_num)):
                    packet_to_send = str(self.seq_num).encode('utf-8') + actual_packet[int(i * self.mtu_len): (
                                int(i * self.mtu_len) + self.mtu_len)]
                    self.send_segment(packet_to_send, len(packet_to_send))
                    # @TODO receive response, may not receive
                    while True:
                        print("Try polling...")
                        socks = dict(self.nw_obj.get_poller().poll(300))
                        if self.nw_obj.get_socket() in socks:
                            print("has response")
                            recv_seq_num = int(self.recv_segment().decode('utf-8')[0])
                            if recv_seq_num == self.seq_num:
                                self.seq_num = (self.seq_num + 1) % 2
                            else:
                                i -= 1
                            break
                        else:
                            print("no response")
                            self.send_segment(packet_to_send, len(packet_to_send))
                print("All the chunks all sent...")
                # stable transmission
                self.nw_obj.send_packet(b'', 0, True)  # to notify that all chunks are sent
        except Exception as e:
            raise e

    ##################################
    #  send transport layer segment
    ##################################
    def send_segment(self, segment, len=0, normal=True):
        try:
            # For this assignment, we ask our dummy network layer to
            # send it to peer. We ignore the length in this assignment
            print("Custom Transport Protocol::send_transport_segment")
            # if not breaking into chunks
            if normal:
                self.nw_obj.send_packet(segment, len)
            else:
                self.nw_obj.send_packet(segment, len)
                self.nw_obj.recv_packet(len)  # get receiver's respond to this single packet

        except Exception as e:
            raise e

    ######################################
    #  receive application-level message
    ######################################
    def recv_appln_msg(self, length=0, normal=True):
        try:
            # The transport protocol (at least TCP) is byte stream, which means it does not
            # know the boundaries of the message. So it must be told how much to receive
            # to make up a meaningful message. In reality, a transport layer will receive
            # all the segments that make up a meaningful message, assemble it in the correct
            # order and only then pass it up to the caller.
            print("Custom Transport Protocol::recv_appln_msg")
            if normal:
                appln_msg = self.recv_segment()
            else:
                appln_msg = b''
                while len(appln_msg) < self.packet_size:
                    chunk = self.recv_segment(0)
                    recv_seq_num = int(chunk.decode('utf-8')[0])
                    print("Received seq num: " + str(recv_seq_num))
                    if recv_seq_num == self.seq_num:
                        self.seq_num = (self.seq_num + 1) % 2
                        appln_msg += chunk[1:1 + self.mtu_len]
                        # @TODO send response
                        print("Now the size is " + str(len(appln_msg)))
                    self.send_segment((str(recv_seq_num)).encode('utf-8'))

                print("Finally the size of packet is " + str(len(appln_msg)) + ".")
                print(appln_msg.decode("utf-8"))
                self.recv_segment()  # respond
                appln_msg = appln_msg[self.digit_of_original_packet: self.digit_of_original_packet + int(
                    appln_msg[0:self.digit_of_original_packet])]
            return appln_msg
        except Exception as e:
            raise e

    ######################################
    #  receive transport segment
    ######################################
    def recv_segment(self, len=0, normal=True):
        try:
            # receive a segment. In future assignments, we may be asking for
            # a pipeline of segments.
            #
            # For this assignment, we do not care about all these things.
            print("Custom Transport Protocol::recv_transport_segment")
            if normal:
                segment = self.nw_obj.recv_packet(len)
            else:
                segment = self.nw_obj.recv_packet(len)
                self.nw_obj.send_packet(b'', 0)  # send respond to received segment
            return segment

        except Exception as e:
            raise e
