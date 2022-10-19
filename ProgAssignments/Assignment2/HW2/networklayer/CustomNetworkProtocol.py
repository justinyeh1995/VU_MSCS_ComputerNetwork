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
import os     # for OS functions
import sys    # for syspath and system exception
import socket # get host ip addr
# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

# import the zeromq capabilities
import zmq

############################################
#  Bunch of Network Layer Exceptions
#
# @TODO@ Add whatever make sense here.
############################################

############################################
#       Custom Network Protocol class
############################################
class CustomNetworkProtocol ():
  '''Custom Network Protocol'''

  ###############################
  # constructor
  ###############################
  def __init__ (self):
    self.role = None  # indicates if we are client or server, false => client
    self.config = None # network configuration
    self.ctx = None # ZMQ context
    self.socket = None  # At this stage we do not know if more than one socket needs to be maintained
    
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, role, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Network Protocol Object: Initialize")
      self.config = config
      self.role = role
      self.ip = ip
      self.port = port
    
      # initialize our variables
      print ("Custom Network Protocol Object: Initialize - get ZeroMQ context")
      self.ctx = zmq.Context ()

      # initialize the config object
      
      # initialize our ZMQ socket
      #
      # @TODO@
      # Note that in a subsequent assignment, we will need to move on to a
      # different ZMQ socket pair, which supports asynchronous transport. In those
      # assignments we may be using the DEALER-ROUTER pair instead of REQ-REP
      #
      # For now, we are fine.
      if (self.role):
        # we are the server side
        print ("Custom Network Protocol Object: Initialize - get REP socket")
        self.socket = self.ctx.socket (zmq.REP)

        # since we are server, we bind
        bind_str = "tcp://" + self.ip + ":" + str (self.port)
        print ("Custom Network Protocol Object: Initialize - bind socket to {}".format (bind_str))
        self.socket.bind (bind_str)
        
      else:
        # we are the client side
        print ("Custom Network Protocol Object: Initialize - get REQ socket")
        self.socket = self.ctx.socket (zmq.REQ)

        # since we are client, we connect
        
        ##########################
        ## Need to Look Up here ##
        ##########################

        connect_str = "tcp://" + self.ip + ":" + str (self.port)
        print ("Custom Network Protocol Object: Initialize - connect socket to {}".format (connect_str))
        self.socket.connect (connect_str)
        
      
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send network packet
  ##################################
  def send_packet (self, packet, size):
    try:

      # Here, we simply delegate to our ZMQ socket to send the info
      print ("Custom Network Protocol::send_packet")
      # @TODO@ - this may need mod depending on json or serialized packet
      if self.config["Application"]["Serialization"] == "json":
        self.socket.send (bytes(packet, "utf-8"))
      else:
        self.socket.send (packet)

    except Exception as e:
      raise e

  ######################################
  #  receive network packet
  ######################################
  def recv_packet (self, len=0):
    try:
      # @TODO@ Note that this method always receives bytes. So if you want to
      # convert to json, some mods will be needed here. Use the config.ini file.
      packet = self.socket.recv ()
      return packet
    except Exception as e:
      raise e

