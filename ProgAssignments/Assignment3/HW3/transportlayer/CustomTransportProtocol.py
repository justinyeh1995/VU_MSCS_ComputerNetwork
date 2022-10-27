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
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Transport Protocol Object: Initialize")
    
      # initialize our variables
      self.ip = ip
      self.port = port

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
      self.nw_obj.initialize (config, self.role, self.ip, self.port)
      
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, payload, size):
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

      ###################
      ## MTU = 16bytes ##
      ## Break 1MB to  ##
      ## 64 chunks &   ##
      ## Add ser. num  ##
      ###################
      print ("Custom Transport Protocol::send_appln_msg")
      self.send_segment (payload, size)
      
      mtu = 16
      fullpacket = [payload[i:i + mtu] for i in range(0, len(payload), mtu)]
      #########
      ## ABP ##
      #########
      l, r = 0 # left, right pointers for sliding window.
      seq_no = 0
      while seq_no < len(fullpacket): # send segment one by one
        token = ''
        # attemp to recv seq_no & ACK
        while token != 'ACK':
         decision = random.randint(1,3) 
         self.send_segment(seq_no, fullpacket[seq_no], decision) # keep resending until we establish handshakes
         seq_no, token = self.recv_ACK(seq_no) # token can be '' or 'ACK' and it might wait for certain amount of time 
        # handshake established
        print (f"Hankshake established for {seq_no}")
        seq_no += 1

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
      self.nw_obj.send_packet ((seq_no, 'ACK'),len)
      
    except Exception as e:
      raise e

  ############################
  ## Used in Sender(Client) ##
  ############################

  def recv_ACK(self, seq_no):
    try:
      # receive an ACK to build handshake
      print ("Custom Transport Protocol::recv_transport_ACK")
      timeout = 10 / 1000
      start = end = time.time()
      token = ''
      while (start - end) <= timeout:
        try:
          seq_no, token = self.nw_obj.recv_packet (len)
          print ("Recieved ACK from the server")
        except zmq.Again as e:
          print ("No message received yet")

        end = time.time()

      return seq_no, token
    
    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment  #
  ##################################
  def send_segment (self, seq_no, segment, decision, len=0): # I modified the parameters 
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print (f"Custom Transport Protocol::send_transport_segment_with_the_{decision}_scenario")
      if decision == 1: # normal behavior
        print("sent to the next hop")
        self.nw_obj.send_packet ((seq_no, segment),len)
      elif decision == 2: # delay
        print(f"dealy for {self.delay} ms")
        time.sleep(self.delay/1000)
        print("sent to the next hop")
        self.nw_obj.send_packet ((seq_no, segment),len)
      else:
        print("segment loss") # loss segment
      
    except Exception as e:
      raise e

  ######################################
  #  receive application-level message
  ######################################
  def recv_appln_msg (self, len=0):
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
      '''
      appln_msg = self.recv_segment ()
      '''

      appln_msg = []
      buffer_SW = [] # buffer for current sliding window
      while True:
          (seq_no, segment) = self.recv_segment () # reciever doesn't know whether there is a loss.
          print(f'No. {seq_no} segment recieved')
          self.send_ACK(seq_no)
          print(f'Sent No. {seq_no} & ACK')
          
          ## for ABP there will be duplicate recieving issues 
          ## handle it here before append it to appln_msg
          ## TO-DO

          appln_msg.append(segment)
          # TO-DO #
          # work with buffers for GBN / SR algo here

      appln_msg = b''.join(appln_msg) # need to print out & check here

      return appln_msg
    
    except Exception as e:
      raise e

  ######################################
  #  receive transport segment
  ######################################
  def recv_segment (self, len=0):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_transport_segment")
      segment = self.nw_obj.recv_packet (len)
      return segment
    
    except Exception as e:
      raise e

