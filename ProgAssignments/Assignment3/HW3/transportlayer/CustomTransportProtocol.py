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
import os     # for OS functions
import sys    # for syspath and system exception
import random
import time
import zmq
import numpy as np
from collections import OrderedDict
import concurrent.futures # for constructing a functional timer
from threading import Event # for constructing a functional timer

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj

############################################
#  Bunch of Transport Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################

############################################
#       Custom Transport Protocol class
############################################
class CustomTransportProtocol ():
  '''Custom Transport Protocol'''

  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client or server, false => client
    self.ip = None
    self.port = None
    self.nw_obj = None # handle to our underlying network layer object
    self.delay = 5
    #########################
    ## Set a timer here ?? ##
    #########################

  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port, router=True):
    ''' Initialize the object '''
    try:
      # Here we initialize any internal variables
      print ("Custom Transport Protocol Object: Initialize")
    
      # initialize our variables
      self.ip = ip
      self.port = port
      self.protocol = config["TCP"]["Protocol"]
      # in a subsequent assignment, we will use the max segment size for our
      # transport protocol. This will be passed in the config.ini file.
      # Right now we do not care.
      
      # Now obtain our network layer object
      print ("Custom Transport Protocol::initialize - obtain network object")
      self.nw_obj = NWProtoObj ()
      
      # initialize it
      # 
      # In this assignment, we let network layer (which holds all the ZMQ logic) to
      # directly talk to the remote peer. In future assignments, this will be the
      # next hop router to whom we talk to.
      print ("Custom Transport Protocol::initialize - initialize network object")
      self.nw_obj.initialize (config, self.role, self.ip, self.port, router)
      
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, payload, size, split):
    try:
      # @TODO@ Implement this
      # What we should get here is a serialized message from the application
      # layer along with the payload size. Now, depending on what is the
      # maximum segment size allowed by our transport, we will need to break the
      # total message into chunks of segment size and send segment by segment.
      # But we will do all this when we are implementing our custom transport
      # protocol. For Assignment #1, we send the entire message as is in a single
      # segment

      ############
      ## Sender ##
      ############
      if not split:
        print ("Custom Transport Protocol::send_appln_msg without chunking it")
        self.send_segment (0, payload, 1, split, size)
      ###################
      ## MTU = 16bytes ##
      ## Break 1MB to  ##
      ## 64 chunks &   ##
      ## Add ser. num  ##
      ###################
      else:
        print ("Custom Transport Protocol::send_appln_msg with chunks")
        mtu = 16
        fullpacket = [payload[i:i + mtu] for i in range(0, len(payload), mtu)]

        #########
        ## ABP ##
        #########

        if self.protocol == "ABP":
          print("ABP")
          seq_no = 0
          while seq_no < len(fullpacket): # send segment one by one
            token = ''
            # attemp to recv seq_no & ACK
            while token != b'ACK':
             print(f"Sending Segment {seq_no}")
             print(fullpacket[seq_no])
             ###############################
             ## The logic is a bit odd rn ##
             ###############################
             self.send_segment (seq_no, fullpacket[seq_no], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size) # keep resending until we establish handshakes

             #################
             ## Add timeout ##
             #################
             seq_no_recv, token = self.recv_ACK(timeout=2000) # token can be '' or 'ACK' and it might wait for certain amount of time 
            
            if token == b"ACK" and seq_no_recv == seq_no: # handshake established
              print (f"Hankshake established for {seq_no}")
              seq_no += 1

        #########
        ## GBN ##
        #########

        elif self.protocol == "GBN":
          print("GO-BACK-N")
          N = 8
          base = 0
          lastpacket = len(fullpacket) - 1

          for i in range(N):
            print(f"Sending {i}-th segment")
            self.send_segment (i, fullpacket[i], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size) # keep resending until we establish handshakes

          while True:
            print("Our Main Purpose")
            seq_recv, token = self.recv_ACK(timeout=2000) # token can be '' or 'ACK' and it might wait for certain amount of time 
            print(f"Custom Transport Layer at Client got {seq_recv}, {token}")
            if seq_recv == base:
              base += 1
              nextpacket = base+N-1
              if nextpacket <= lastpacket:
                self.send_segment (nextpacket, fullpacket[nextpacket], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size)
                print(f"Sending {base+N-1}-th segment")
            elif seq_recv == base - 1:
              print ("Duplicate ACK")
            else:
              assert seq_recv == -1
              print(f"Go-Back-{base}")
              for i in range(base,min(base+N,64)):
                self.send_segment (i, fullpacket[i], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size) 
                print(f"Resending {i}-th segment")
            if base == len(fullpacket):
              print("Done!")
              break

        ########
        ## SR ##
        ########

        elif self.protocol == "SR":
          '''
          keeps track of wR and ensures that wR > ( snd_next − snd_una)
          retransmits only unACKed packets
          '''
          '''
          if next available seq# in window, send packet
          timeout(n)-> resend packet n and restart timer
          received ACK(n) in [send_una, send_next]:
            mark pkt n as recrived
            if n is the smallest unACKed pkt, advance send_una to next unACKed seq#
          '''
          print("SR")
          N = 8
          base = 0 # the smallest seq# unACK pkt
          lastpacket = len(fullpacket) - 1
          unACK = set() # cannot exceed window size(N)
          sent = 0

          for i in range(N):
            print(f"Sending {i}-th segment")
            self.send_segment (i, fullpacket[i], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size) # keep resending until we establish handshakes
            unACK.add(i)
            sent += 1

          base = min(unACK) #0
          send_next = base + N #4

          while True:
            print("Our Main Purpose")
              
            seq_recv, token = self.recv_ACK(timeout=2000) # token can be '' or 'ACK' and it might wait for certain amount of time 
            print(f"Custom Transport Layer at Client got ACK {seq_recv}, {token}")

            if (
                (seq_recv == base or (send_next - base) < N) 
                and send_next <= lastpacket
                ):
              print ("We still have room for sending the next pkt")
              self.send_segment (send_next, fullpacket[send_next], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size)
              unACK.add(send_next)
              send_next += 1
              
              sent += 1
              
            else:
              print (f"Ignore. Don't send anything..")

            if seq_recv in unACK and seq_recv in range(base, send_next+1):
              print (f"Custom Transport Layer at Client remove {seq_recv} in buffer")
              unACK.remove(seq_recv) # remove unACK(seq_recv) from buffer
              if unACK:
                if base == min(unACK):
                  print (f"Base stays the same")
                else:
                  print (f"base from {base} to {min(unACK)}")
                  base = min(unACK)

            ############################
            ## Retransmit timeout pkt ##
            ############################
            ## TO-DO ##
            for seq in sorted(unACK):
              if seq_recv > seq:
                self.send_segment (seq, fullpacket[seq], random.choices([1,2,3],[0.85,0.15,0.00])[0], split, size)
                sent += 1
            # edge cases: unsure if the logic holds
            #if seq_recv == -1:
            #  self.send_segment (base, fullpacket[base], random.choices([1,2,3],[0.85,0.1,0.05])[0], split, size)
            #  unACK.add(base) #??
            print(sent)
            ########################
            ## Stopping condition ##
            ########################
            ## TO-DO ##
            if not unACK:
              break

        print("sending dummy message")
        self.send_segment (0, b'dummy', 1, split=False) # not sure why we should do this but I kept failing without this further step

      print("All segments sent!")
        
    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment  #
  ##################################
  def send_segment (self, seq_no, segment, decision, split, size=0): # I modified the parameters 
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print (f"Custom Transport Protocol::send_transport_segment_with_the_{decision}_scenario")
      if decision == 1: # normal behavior
        print("Packet sent to the next hop :>>")
        self.nw_obj.send_packet ((seq_no, segment), size, split)
      elif decision == 2: # delay
        print(f"Delay sending for {self.delay} ms")
        time.sleep(self.delay/1000)
        print("After delaying for {self.delay} ms, send the packet to the next hop")
        self.nw_obj.send_packet ((seq_no, segment), size, split)
      else:
        print("Packet loss!!") # loss segment
      
    except Exception as e:
      raise e
  
  ##############################
  ## Used in Reciever(Server) ##
  ##############################

  def send_ACK(self,seq_no):
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print ("Custom Transport Protocol::send_transport_segment_ACK")
      self.nw_obj.send_packet_ACK ((seq_no, 'ACK'.encode()),len)
      
    except Exception as e:
      raise e

  ############################
  ## Used in Sender(Client) ##
  ############################

  def recv_ACK(self, timeout=2000):
    try:
      # receive an ACK to build handshake
      print ("Custom Transport Protocol::recv_transport_ACK")
      #########################
      ## Set Up Timeout Here ##
      #########################
      seq_no, token = self.nw_obj.recv_packet_ACK (timeout=timeout)
      return seq_no, token
    
    except Exception as e:
      raise e

  ######################################
  #  receive application-level message
  ######################################
  def recv_appln_msg (self, size=0, split=False):
    try:
      # The transport protocol (at least TCP) is byte stream, which means it does not
      # know the boundaries of the message. So it must be told how much to receive
      # to make up a meaningful message. In reality, a transport layer will receive
      # all the segments that make up a meaningful message, assemble it in the correct
      # order and only then pass it up to the caller.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_transport_segment")
      ##############
      ## Reciever ##
      ##############

      ################################
      ## Make sure it is a full msg ##
      ################################
      if not split:
        appln_msg = self.recv_segment (split)
      else:
        appln_msg = []
        
        #########
        ## ABP ##
        #########

        if self.protocol == "ABP":
          print("ABP")
          while True:
            seq_no, segment = self.recv_segment (split) # reciever doesn't know whether there is a loss.
            print(f'No. {seq_no} segment recieved')
            self.send_ACK(seq_no)
            print(f'Sent No. {seq_no} & ACK')
            
            ## for ABP there will be duplicate recieving issues 
            ## handle it here before append it to appln_msg
            ##############################
            ## Handle duplicate packets ##
            ##############################
            if seq_no < len(appln_msg):
              continue

            ########################
            ## Stopping Condition ##
            ########################
            appln_msg.append(segment)
            if len(appln_msg) >= 64:
              print("Recieve All")
              break
            
        #########
        ## GBN ##
        #########

        elif self.protocol == "GBN":
          print("GO-BACK-N")
          expect_recv = 0
          while True:
            # recieve msg from the client/router
            recv_no, segment = self.recv_segment (split) # if packet is lost -> recv = -1 , out of order recv
            print(f'No. {recv_no} segment recieved')
            if recv_no == expect_recv:
              appln_msg.append(segment)
              self.send_ACK(recv_no)
              expect_recv += 1
              print("In-Order packet")
              print(f'Sent No. {recv_no} & ACK')
              print(f"Expect to get {expect_recv}")
            else:
              if expect_recv > 0:
                in_order = expect_recv - 1
                self.send_ACK(in_order)
                print("Out of Order packet :(( Discard it! \n Resend {in_order} ACK")

            ########################
            ## Stopping Condition ##
            ########################
            if len(appln_msg) >= 64:
              print("Recieve All")
              break

        ########
        ## SR ##
        ########

        elif self.protocol == "SR":
          '''
          buffers out-of-order packets (up to wR), for in-order delivery
          ACKs all correctly (no error, but may be out-of-order) received packets individually, not cumulatively
          '''
          print("SR")
          expect_recv = 0
          base = 0
          buff = []
          buff_size = 8
          buff = OrderedDict()
 
          recv = 0
          while True:
            recv_no, segment = self.recv_segment (split) # in order or out of order recv_no
            recv += 1
            print(recv)
            print(f'No. {recv_no} segment recieved')
            if recv_no in range(expect_recv, expect_recv+buff_size):

              self.send_ACK(recv_no)
              
              # in-order
              if recv_no == expect_recv:
                appln_msg.append(segment)
                expect_recv += 1
                print ("In-Order packet")
                print (f'Sent No. {recv_no} & ACK')
                print (f"Expect to get {expect_recv}")
                print ("Lets check the buffer as well")
                for seq, seg in buff.items():
                  appln_msg.append(seg)
                # flush
                buff = OrderedDict()
                    
              # out-of-order
              # do not move the window
              else:
                print("Out of Order packet :(( Let's buffer them")
                if len(buff) < buff_size:
                  buff[recv_no] = segment

            elif recv_no < expect_recv:
              print ("recv_no < than expect_recv {expect_recv}")
              #self.send_ACK(recv_no)

            else:
              print ("Ignore it...")

            ########################
            ## Stopping Condition ##
            ########################
            if len(appln_msg) >= 64:
              print("Recieve All")
              break
          

        ##################
        ## Assemble Msg ##
        ##################
        appln_msg = b''.join(appln_msg) # need to print out & check here
        dummy = self.recv_segment (split=False) # not sure
      print ("===================================")
      print ("Recieved full messages")
      print (appln_msg)
      return appln_msg
    
    except Exception as e:
      raise e

  ######################################
  #  receive transport segment
  ######################################
  def recv_segment (self, split, size=0):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      if not split:
        segment = self.nw_obj.recv_packet (split, size)
        return segment

      seq_no ,segment = self.nw_obj.recv_packet (split, size)
      return seq_no, segment
    
    except Exception as e:
      print("Error at transport layer::rev_segment") 
      raise e

