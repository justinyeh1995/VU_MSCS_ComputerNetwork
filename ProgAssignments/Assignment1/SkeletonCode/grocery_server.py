# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for the Smart Refrigerator server
#          needed for the Computer Networks course Assignments. This one handles
#          grocery order requests
#
#          Since we are hoping to develop a very crude networking stack
#          in this course, we will see that our server uses an Application
#          layer object instead of directly using the ZeroMQ socket API, which
#          is used under the hood at some layer.  That in turn uses a Transport
#          object and so on.
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import time   # for sleep
import argparse # for argument parsing
import configparser # for configuration parsing
import zmq # actually not needed here but we are printing zmq version and hence needed
import serialize_flatbuffer as szbf  # this is from the file serialize.py in the same directory
import serialize_json as szjs  # this is from the file serialize.py in the same directory

# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage

##################################
#   Health Status Server class
##################################
class GroceryOrder ():
  '''GroceryOrder Server'''
  
  ########################################
  # constructor
  ########################################
  def __init__ (self):
    self.grocery_obj = None
    self.ser_type = "json"

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("GroceryOrder Object: Initialize")
    
      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
    
      # Next, obtain the custom application protocol object
      self.grocery_obj = ApplnProtoObj (True)  # the True flag indicates this is a server side

      # initialize the custom application objects
      self.grocery_obj.initialize (config, args.addr, args.port)
        
      # not sure this workflow is good enough
      self.ser_type = config["Application"]["Serialization"]


    except Exception as e:
      raise e

  ########################################
  #  A generator of the response message
  ########################################
  def gen_response_msg (self):
    '''Response message generator '''

    # @TODO@ Add code here.
    #
    # Basically, a response msg is very simple. Set the message type and message
    
    resp_msg = ResponseMessage ()
    resp_msg.type = "RESPONSE"
    # fill up the fields in whatever way you want
    
    return resp_msg
  
  ##################################
  # Driver program
  ##################################
  def driver (self):
    try:
      # The health status server will run forever
      while True:
        # receive a request. If we do not understand it, send a BadRequest response
        # else send a valid response
        # @TODO
        # For now we send a dummy response

        request = self.grocery_obj.recv_request () # request is a buffer
        print ("Received request: {}".format (request))
        # @handle the request here, including those bad requests
        """ deserialize here"""
        """if ...: do sth // else: send badRequest"""
        ### check type
        if self.ser_type == "fbufs" and szfb.checktype(request) == b"ORDER":
            resp_msg = szfb.deserialize(request)
            #resp_msg.addCode(random.randint(1,2)) # just for now 
            #resp_msg.code = "OK": 
            #resp_msg.contents = "Your order is placed!"
            resp = self.gen_response_msg ()
            resp.type = "RESPONSE"
            resp.code = "OK"
            resp.contents = "Your order is placed!"
        elif self.ser_type == "json" and szjs.checktype(request) == "ORDER":
            resp_msg = szjs.deserialize(request)
            #resp_msg.addCode(random.randint(1,2)) # just for now 
            #resp_msg.code = "OK": 
            #resp_msg.contents = "Your order is placed!"
            resp = self.gen_response_msg ()
            resp.type = "RESPONSE"
            resp.code = "OK"
            resp.contents = "Your order is placed!"
        else:
            resp = self.gen_response_msg ()
            resp.type = "RESPONSE"
            resp.code = "BAD_REQUEST"
            resp.contents = "Bad Request!"

        self.grocery_obj.send_response (resp)
        
    except Exception as e:
      raise e

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ("Argument parser for the health status server")

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-a", "--addr", default="*", help="Interface we are accepting connections on (default: all)")
  parser.add_argument ("-p", "--port", type=int, default=5555, help="Port the health status server is listening on (default: 5555)")
  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  try:
    print("Skeleton Code for the GroceryOrder Server")

    # first parse the command line args
    print ("GroceryOrder main: parsing command line")
    parsed_args = parseCmdLineArgs ()
    
    # Obtain a health status server object
    print ("GroceryOrder main: obtain the object")
    hs = GroceryOrder ()

    # initialize our refrigerator object
    print ("GroceryOrder main: initialize the object")
    hs.initialize (parsed_args)

    # Now drive the rest of the assignment
    print ("GroceryOrder main: invoke driver")
    hs.driver ()

    # we are done. collect results and do the plotting etc.
    #
    # @TODO@ Add code here.
  except Exception as e:
    print ("Exception caught in main - {}".format (e))
    return

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
