# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom application protocol
#          used by our smart refrigerator to send grocery order and health status
#          messages. This is our Application Layer used in the Computer Networks
#          course Assignments
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import time   # for sleep
from enum import Enum  # for enumerated types
import subprocess
import re
import pandas as pd

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from transportlayer.CustomTransportProtocol import CustomTransportProtocol as XPortProtoObj
import serialize_flatbuffer as szfb  # this is from the file serialize.py in the same directory
import serialize_json as szjs  # this is from the file serialize.py in the same directory

testDB = pd.read_csv("./RouteDB.csv")

############################################
#  Serialization Enumeration Type
############################################
class SerializationType (Enum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  JSON = 1
  FBUFS = 2

############################################
#  Bunch of Application Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################
class BadSerializationType (Exception):
  '''Bad Serialization Type'''
  def __init__ (self, arg):
    msg = arg + " is not a known serialization type"
    super ().__init__ (msg)

class BadMessageType (Exception):
  '''Bad Message Type'''
  def __init__ (self):
    msg = "bad or unknown message type"
    super ().__init__ (msg)

############################################
#       Custom Application Protocol class
############################################
class CustomApplnProtocol ():
  '''Custom Application Protocol for the Smart Refrigerator'''

  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client or server, false => client
    self.ser_type = SerializationType.UNKNOWN
    self.xport_obj = None # handle to our underlying transport layer object
    
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Application Protocol Object: Initialize")
      print ("serialization type = {}".format (config["Application"]["Serialization"]))
    
      # initialize our variables
      if (config["Application"]["Serialization"] == "json"):
        self.ser_type = SerializationType.JSON
      elif (config["Application"]["Serialization"] == "fbufs"):
        self.ser_type = SerializationType.FBUFS
      else:  # Unknown; raise exception
        raise BadSerializationType (config["Application"]["Serialization"])

      # Now obtain our transport object
      # @TODO
      print ("Custom Appln Protocol::initialize - obtain transport object")
      self.xport_obj = XPortProtoObj (self.role)

      # initialize it
      print ("Custom Appln Protocol::initialize - initialize transport object")
      ### TO-DO: add next ip here
      self.xport_obj.initialize (config, ip, port)
      
    except Exception as e:
      raise e  # just propagate it

    
  ##################################
  #  send Grocery Order
  ##################################
  def send_grocery_order (self, order):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Grocery Order supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is grocery order else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if order.type == "ORDER":
        #@TODO@ Implement this
        print ("serialize the message")
        start_time = time.time ()
        if self.ser_type == SerializationType.JSON:
            buf = szjs.serialize (order)
        else:
            buf = szfb.serialize (order)
        end_time = time.time ()
        print ("Serialization took {} secs".format (end_time-start_time))

      else:  # Unknown; raise exception
        raise BadMessageType ()
      print(type(buf))
      self.xport_obj.send_appln_msg (buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  send Health Status
  ##################################
  def send_health_status (self, status):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Health Status supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is health status else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if status.type == "HEALTH":
        #@TODO@ Implement this
        print ("serialize the message")
        start_time = time.time ()
        if self.ser_type == SerializationType.JSON:
            buf = szjs.serialize (status)
        else:
            buf = szfb.serialize (status)
        end_time = time.time ()
        print ("Serialization took {} secs".format (end_time-start_time))

      else:  # Unknown; raise exception
        raise BadMessageType ()

      self.xport_obj.send_appln_msg (buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  send response
  ##################################
  def send_response (self, response):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Health Status supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is response else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if response.type == "RESPONSE":
        #@TODO@ Implement this
        print ("serialize the message")
        start_time = time.time ()
        if self.ser_type == SerializationType.JSON:
            buf = szjs.serialize (response)
        else:
            buf = szfb.serialize (response)
        end_time = time.time ()
        print ("Serialization took {} secs".format (end_time-start_time))

      else:  # Unknown; raise exception
        raise BadMessageType ()

      self.xport_obj.send_appln_msg (buf, len (buf))
    except Exception as e:
      raise e

  ##################################
  #  receive request
  ##################################
  def recv_request (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      request = self.xport_obj.recv_appln_msg ()
      if self.ser_type == SerializationType.FBUFS:
        request = szfb.deserialize(request)
      else:
        request = szjs.deserialize(request)
      return request
    except Exception as e:
      raise e

  ##################################
  #  receive response
  ##################################
  def recv_response (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      response = self.xport_obj.recv_appln_msg ()
      if self.ser_type == SerializationType.FBUFS:
        response = szfb.deserialize(response)
      else:
        response = szjs.deserialize(response)
      return response
    except Exception as e:
      raise e

