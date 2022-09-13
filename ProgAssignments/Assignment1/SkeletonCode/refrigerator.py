# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for the Smart Refrigerator client
#          needed for the Computer Networks course Assignments
#
#          Since we are hoping to develop a very crude networking stack
#          in this course, we will see that our client uses an Application
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

# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage

##################################
#       Refrigerator class
##################################
class Refrigerator ():

  ########################################
  # constructor
  ########################################
  def __init__ (self):
    self.iters = None
    self.req_ratio = None
    self.groc_obj = None
    self.health_obj = None

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Refrigerator Object: Initialize")
    
      # initialize our variables
      self.iters = args.iters
      self.req_ratio = args.req_ratio

      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
    
      # Next, obtain the custom application protocol objects
      self.groc_obj = ApplnProtoObj (False)  # the false flag indicates this is a client side
      self.health_obj = ApplnProtoObj (False)  # the false flag indicates this is a client side

      # initialize the custom application objects
      self.groc_obj.initialize (config, args.groc_ip, args.groc_port)
      self.health_obj.initialize (config, args.status_ip, args.status_port)

    except Exception as e:
      raise e

  ########################################
  #  A generator of the grocery message
  ########################################
  def gen_grocery_order_msg (self):
    '''Grocery order message generator '''

    # @TODO@ Add code here.
    #
    # Basically, use some random number or any such logic and create a grocery message.
    # We do not care about its contents.
    
    groc_msg = GroceryOrderMessage ()
    # fill up the fields in whatever way you want
    
    return groc_msg
  
  ########################################
  #  A generator of the health status message
  ########################################
  def gen_health_status_msg (self):
    '''Status message generator '''

    # @TODO@ Add code here.
    #
    # Basically, use some random number or any such logic and create a status message.
    # We do not care about its contents.
    
    status_msg = HealthStatusMessage ()
    # fill up the fields in whatever way you want
    
    return status_msg
  
  ##################################
  # Driver program
  ##################################
  def driver (self):
    try:

      # To ensure that bad requests are handled correctly, initially let us first
      # try sending wrong message to wrong server.

      # Test 1:
      # create a grocery order
      msg = self.gen_grocery_order_msg ()
      print ("Sending grocery msg to health server {}".format (msg))
      # send it to health server and see if we get a bad request reply
      self.health_obj.send_grocery_order (msg)
      # now receive a response
      reply = self.health_obj.recv_response () 
      print ("Received reply {}".format (reply))

      # Test 2:
      # create a health status
      msg = self.gen_health_status_msg ()
      print ("Sending health msg to grocery server {}".format (msg))
      # send it to grocery server and see if we get a bad request reply
      self.groc_obj.send_health_status (msg)
      # now receive a response
      reply = self.groc_obj.recv_response () 
      print ("Received reply {}".format (reply))
      
      # Test 3: 
      # Here in each iteration and depending on the ratio, we decide whether to
      # send Grocery Message or Health Status Message. These are sent correctly. 
      #
      # @TODO - 
      # Sending messages as per the ratio is not such a big deal for this assignment.
      # Just alternating between the two is fine. What we really care is that both
      # kinds of message types can be sent, and that if they received by the right
      # server, we get a success response. Time the result.

      for i in range (self.iters):
        if (i % 2) == 0:
          # create a grocery order
          msg = self.gen_grocery_order_msg ()
          print ("Sending grocery msg to grocery server {}".format (msg))
          # send it to health server and see if we get a bad request reply
          self.groc_obj.send_grocery_order (msg)
          # now receive a response
          print ("Waiting for response")
          response = self.groc_obj.recv_response () 
          print ("Received reply {}".format (response))
        else:
          # create a health status
          msg = self.gen_health_status_msg ()
          print ("Sending health msg to health server {}".format (msg))
          # send it to grocery server and see if we get a bad request reply
          self.health_obj.send_health_status (msg)
          # now receive a response
          print ("Waiting for response")
          response = self.health_obj.recv_response () 
          print ("Received reply {}".format (response))

        # some delay between requests
        time.sleep (1)
      
    except Exception as e:
      raise e

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ("Argument parser for the refrigerator client")

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
  parser.add_argument ("-g", "--groc_ip", default="127.0.0.1", help="IP Address of Grocery server to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-p", "--groc_port", type=int, default=5555, help="Port that grocery server is listening on (default: 5555)")
  parser.add_argument ("-s", "--status_ip", default="127.0.0.1", help="IP Address of Health Status server to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-q", "--status_port", type=int, default=7777, help="Port that Healt Status server is listening on (default: 7777)")
  parser.add_argument ("-r", "--req_ratio", default="1:1", help="Ratio of grocery orders sent to health status (default: 1:1 implying equal number)")
  
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  try:
    print("Skeleton Code for the Refrigerator Client")

    # first parse the command line args
    print ("Refrigerator main: parsing command line")
    parsed_args = parseCmdLineArgs ()
    
    # Obtain a refrigerator object
    print ("Refrigerator main: obtain the object")
    fridge = Refrigerator ()

    # initialize our refrigerator object
    print ("Refrigerator main: initialize the object")
    fridge.initialize (parsed_args)

    # Now drive the rest of the assignment
    print ("Refrigerator main: invoke driver")
    fridge.driver ()

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
