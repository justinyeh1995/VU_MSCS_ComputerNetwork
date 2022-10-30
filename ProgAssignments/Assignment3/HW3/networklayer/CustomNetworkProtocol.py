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
import re
import subprocess
import pandas as pd

############################################
#  Bunch of Network Layer Exceptions
#
# @TODO@ Add whatever make sense here.
############################################
testDB = pd.read_csv("./RouteDB.csv")
ip2host = {f"10.0.0.{i}": f"H{i}" for i in range(1,30)}
host2ip = { f"H{i}": f"10.0.0.{i}" for i in range(1,30)}

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
        ############
        ## Assign ##
        ############
        # since we are client, we connect
        try:
          self.socket = self.ctx.socket (zmq.REQ)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error obtaining context: {}".format (err))
          return
        except:
          print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
          return
        
        '''
        connect_str = "tcp://" + self.ip + ":" + str (self.port)
        print ("Custom Network Protocol Object: Initialize - connect socket to {}".format (connect_str))
        self.socket.connect (connect_str)
        '''
        ##################
        ## Set Identity ##
        ##################
        try:
          # set our identity
          final_addr = self.ip + ":" + str(self.port)
          print ("client setting its identity: {}".format (final_addr))
          self.socket.setsockopt (zmq.IDENTITY, bytes (final_addr, "utf-8"))
        except zmq.ZMQError as err:
          print ("ZeroMQ Error setting sockopt: {}".format (err))
          return
        except:
          print ("Some exception occurred setting sockopt on REQ self.socket {}".format (sys.exc_info()[0]))
          return

        ############################
        ## Look Up Next Addr here ##
        ############################
        try:
          ## Get host ip & convert it to host name
          print("Obtaining the Next Hop Host Name")
          ifconfig_output=(subprocess.check_output('ifconfig')).decode()
          regex_ip=re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",ifconfig_output)
          my_ip = str(regex_ip.group(0))
          ## @TO-DO@
          nexthost = testDB.loc[testDB.host==ip2host[my_ip]].loc[testDB.destination==self.ip].nexthop.values[0]
          nexthop = host2ip[nexthost]
          print(f"Router HostName is {nexthop}")
          print(f"Router Host IP is {ip2host[my_ip]}")
        except:
          print ("Some exception occurred getting ROUTER host name...")
          return
        #############
        ## Connect ##
        #############
        try:
          # as in a traditional self.socket, tell the system what IP addr and port are we
          # going to connect to. Here, we are using TCP self.sockets.
          connect_string = "tcp://" + nexthop + ":" + str (4444)
          print ("Custom Network Protocol Object: Initialize - connect self.socket to {}".format (connect_string))
          self.socket.connect (connect_string)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error connecting REQ self.socket: {}".format (err))
          self.socket.close ()
          return
        except:
          print ("Some exception occurred connecting REQ self.socket {}".format (sys.exc_info()[0]))
          self.socket.close ()
          return
            
    except Exception as e:
      raise e  # just propagate it
    
  ##################################
  #  send network packet
  ##################################
  def send_packet (self, segment, size, role):
    try:
      ###### to-do ###########
      ## handle packet here ##
      ########################
      seq_no, packet = segment
      byte_seq_no = (str(seq_no)+'+++').encode()
      # here, we simply delegate to our zmq socket to send the info
      # @todo@ - this may need mod depending on json or serialized packet
      #######################################
      ## constrain the size of packet here ##
      #######################################
      if role == "response":
        print ("custom network protocol::send_packet without chunking")
        #dummy = self.socket.recv () # wtf????
        if self.config["Application"]["Serialization"] == "json":
          self.socket.send (bytes(packet, "utf-8"))
        else:
          self.socket.send (packet)
      else:
        print ("custom network protocol::send_packet with chunks")
        if self.config["Application"]["Serialization"] == "json":
          self.socket.send (byte_seq_no + bytes(packet, "utf-8"))
        else:
          self.socket.send (byte_seq_no + packet)

    except Exception as e:
      raise e

  ##################################
  #  send network packet
  ##################################
  def send_packet_ACK (self, segment, size):
    try:

      ###### to-do ###########
      ## handle packet here ##
      ########################
      seq_no, packet = segment
      byte_seq_no = (str(seq_no)+'+++').encode()
      # here, we simply delegate to our zmq socket to send the info
      print ("custom network protocol::send_packet_ACK")
      # @todo@ - this may need mod depending on json or serialized packet
      #######################################
      ## constrain the size of packet here ##
      #######################################
      self.socket.send (byte_seq_no + packet)

    except Exception as e:
      raise e

  ######################################
  #  receive network packet
  ######################################
  def recv_packet (self, role, len=0):
    try:
      # @TODO@ Note that this method always receives bytes. So if you want to
      # convert to json, some mods will be needed here. Use the config.ini file.
      
      print ("Custom Network Protocol::recv_packet")
      if role == "response":
        print ("Recieving responses or full messages..")
        #self.socket.send (b'dummy') #wtf
        packet = self.socket.recv ()
        return packet
      else:
        print ("Recieving Chunked Messages..")
        packet = self.socket.recv ()
        b_seq_no, payload = packet.split(b"+++")
        return int(b_seq_no.decode()), payload
    except Exception as e:
        print("Error at network layer::recv_packet")
        raise e

