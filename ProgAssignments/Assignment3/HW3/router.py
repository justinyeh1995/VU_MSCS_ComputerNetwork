## this bussiness logic focuses on transpot layer & network layer 
import os
import sys
import time   # for sleep
import argparse # for argument parsing
import configparser # for configuration parsing
import zmq # actually not needed here but we are printing zmq version and hence needed
import subprocess # for calling ifconfig
import re # for parsing first inet addr
import csv # for parsing the routing table
import pandas as pd
# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert (0, os.getcwd ())

from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj

testDB = pd.read_csv("./RouteDB.csv")
##########################################################
#receive a request and simply forward it to the next hop #
# by consulting the supplied route                       #
##########################################################

class CustomRouter ():
  ########################################
  # constructor
  ########################################

  def __init__(self):
    self.router_obj = None
    self.ip2host = {f"10.0.0.{i}": f"H{i}" for i in range(1,10)}
    self.host2ip = { f"H{i}": f"10.0.0.{i}" for i in range(1,10)}
    self.final_dest = None
    self.next_ip = None
    self.next_port = None

  ########################################
  # configure/initialize
  ########################################
  def initialize (self, args):
    '''  
    try:
      # Here we initialize any internal variables
      print ("Router Object: Initialize")
    
      # Now, get the configuration object
      config = configparser.ConfigParser ()
      config.read (args.config)
    
      # Next, obtain the custom application protocol object
      self.router_obj = ApplnProtoObj (True)  # the True flag indicates this is a server side

      # initialize the custom application objects
      self.router_obj.initialize (config, args.addr, args.port)
    '''
    try:
      # every ZMQ session requires a context
      print ("Obtain the ZMQ context")
      context = zmq.Context ()   # returns a singleton object
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining context: {}".format (err))
      return
    except:
      print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
      return

    try:
      # Get a poller object
      print ("Obtain the Poller")
      poller = zmq.Poller ()
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining poller: {}".format (err))
      return
    except:
      print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
      return

    #########################
    ## Bind our own socket ##
    #########################
    try:
      # The socket concept in ZMQ is far more advanced than the traditional socket in
      # networking. Each socket we obtain from the context object must be of a certain
      # type. For TCP, we will use ROUTER for server side (many other pairs are supported
      # in ZMQ for tcp.
      print ("Obtain the ROUTER type socket")
      bind_sock = context.socket (zmq.ROUTER)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error obtaining ROUTER socket: {}".format (err))
      return
    except:
      print ("Some exception occurred getting ROUTER socket {}".format (sys.exc_info()[0]))
      return

    try:
      # as in a traditional socket, tell the system what port are we going to listen on
      # Moreover, tell it which protocol we are going to use, and which network
      # interface we are going to listen for incoming requests. This is TCP.
      print ("Bind the ROUTER socket")
      bind_string = "tcp://" + args.myaddr + ":" + str (args.myport)
      print ("TCP router will be binding on {}".format (bind_string))
      bind_sock.bind (bind_string)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error binding ROUTER socket: {}".format (err))
      bind_sock.close ()
      return
    except:
      print ("Some exception occurred binding ROUTER socket {}".format (sys.exc_info()[0]))
      bind_sock.close ()
      return
    
    ###############################################
    ## Wait on the first REQ for routing purpose ##
    ###############################################

    ########################
    ## Register to Poller ##
    ########################
    try:
      # register sockets
      print ("Register sockets for incoming events")
      poller.register (bind_sock, zmq.POLLIN)
      #poller.register (conn_sock, zmq.POLLIN)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error registering with poller: {}".format (err))
      return
    except:
      print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
      return
    except Exception as e:
      raise e
    

  ##################################
  # Driver program
  ##################################
  def driver (self):
    try:
    # since we are a server, we service incoming clients forever
    print ("Router now starting its forwarding loop")
      while True:
        try:
          # collect all the sockets that are enabled in this iteration
          socks = dict (poller.poll ())
        except zmq.ZMQError as err:
          print ("ZeroMQ Error polling: {}".format (err))
          return
        except:
          print ("Some exception occurred in polling {}".format (sys.exc_info()[0]))
          return

        # Now handle the event for each enabled socket
        if bind_sock in socks:
          # we are here implies that the bind_sock had some info show up.
          try:
            #  Wait for next request from previous hop. When using DEALER/ROUTER, it is suggested to use
            # multipart send/receive. What we receive will comprise the sender's info which we must preserve, an empty
            # byte, and then the actual payload
            request = bind_sock.recv_multipart ()
            print("Router received request from prev hop via ROUTER: %s" % request)
            print(request[-3])
            final_dest = request[-3].decode("utf-8").split("/")[0]
            ###################
            ## Table Look Up ##
            ###################
            print("Consulting the Routing Table...")
            try:
              ## Get host ip & convert it to host name
              print("Obtaining the Next Hop Host Name")
              ifconfig_output=(subprocess.check_output('ifconfig')).decode()
              regex_ip=re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",ifconfig_output)
              my_ip = str(regex_ip.group(0))
              assert my_ip == args.myaddr # just to make sure it's same, i will clean this up later
              ## @TO-DO@
              nexthost = testDB.loc[testDB.host==ip2host[my_ip]].loc[testDB.destination==final_dest].nexthop.values[0] # replace "10.0.0.5" with final destination
              nexthop = host2ip[nexthost]
              print(f"Router HostName is {nexthop}")
              print(f"Router Host IP is {self.ip2host[my_ip]}")
            except:
              print ("Some exception occurred getting ROUTER host name...")
              return
          except zmq.ZMQError as err:
            print ("ZeroMQ Error receiving: {}".format (err))
            bind_sock.close ()
            return
          except:
            print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
            bind_sock.close ()
            return
          #########################
          ## Connect to next hop ##
          #########################
          try:
            # The socket concept in ZMQ is far more advanced than the traditional socket in
            # networking. Each socket we obtain from the context object must be of a certain
            # type. For TCP, we will use the DEALER socket type (many other pairs are supported)
            # and this is to be used on the client side.
            print ("Router acquiring connection socket")
            conn_sock = context.socket (zmq.DEALER)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error obtaining context: {}".format (err))
            return
          except:
            print ("Some exception occurred getting DEALER socket {}".format (sys.exc_info()[0]))
            return

          ##################
          ## Set Identity ##
          ##################
          try:
            # set our identity
            print ("router setting its identity: {}".format (nexthop))
            conn_sock.setsockopt (zmq.IDENTITY, bytes(nexthop, "utf-8")) # the long string should be "H1", "H2" or something
          except zmq.ZMQError as err:
            print ("ZeroMQ Error setting sockopt: {}".format (err))
            return
          except:
            print ("Some exception occurred setting sockopt on REQ socket {}".format (sys.exc_info()[0]))
            return

          ######################################
          ## Connection should be found later ##
          ######################################
          try:
            # as in a traditional socket, tell the system what IP addr and port are we
            # going to connect to. Here, we are using TCP sockets.
            print ("Router connecting to next hop")
            #### TO-DO
            nexthopport = 4444
            connect_string = "tcp://" + nextip + ":" + str (nexthopport)
            print ("TCP client will be connecting to {}".format (connect_string))
            conn_sock.connect (connect_string)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error connecting DEALER socket: {}".format (err))
            conn_sock.close ()
            return
          except:
            print ("Some exception occurred connecting DEALER socket {}".format (sys.exc_info()[0]))
            conn_sock.close ()
            return

          poller.register (conn_sock, zmq.POLLIN)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error registering with poller: {}".format (err))
            return
          except:
            print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
            return
          except Exception as e:
            raise e

          try:
            #  forward request to server
            print ("Forward the same request to next hop over the DEALER")
            conn_sock.send_multipart (request)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error forwarding: {}".format (err))
            conn_sock.close ()
            return
          except:
            print ("Some exception occurred forwarding {}".format (sys.exc_info()[0]))
            conn_sock.close ()
            return

        
        try:
          # collect all the sockets that are enabled in this iteration
          socks = dict (poller.poll ())
        except zmq.ZMQError as err:
          print ("ZeroMQ Error polling: {}".format (err))
          return
        except:
          print ("Some exception occurred in polling {}".format (sys.exc_info()[0]))
          return

        if conn_sock in socks:
          try:
            #  Wait for response from next hop
            response = conn_sock.recv_multipart ()
            print("Router received response from next hop via DEALER: %s" % response)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error receiving response: {}".format (err))
            conn_sock.close ()
            return
          except:
            print ("Some exception occurred receiving response {}".format (sys.exc_info()[0]))
            conn_sock.close ()
            return

          try:
            #  Send reply back to previous hop. request[0] is the original client identity preserved at every hop
            # response[1] has actual payload
            print ("Send reply to prev hop via ROUTER")
            bind_sock.send_multipart (response)
          except zmq.ZMQError as err:
            print ("ZeroMQ Error sending: {}".format (err))
            bind_sock.close ()
            return
          except:
            print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
            bind_sock.close ()
            return

    except Exception as e:
      raise e
  
##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-a", "--myaddr", default="*", help="Interface to bind to (default: *)")
  parser.add_argument ("-p", "--myport", type=int, default=4444, help="Port to bind to (default: 4444)")
  #parser.add_argument ("-A", "--nexthopaddr", default="127.0.0.1", help="IP Address of next router or end server to connect to (default: localhost i.e., 127.0.0.1)")
  #parser.add_argument ("-P", "--nexthopport", type=int, default=4444, help="Port that appln or next router is listening on (default: 4444)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for TCP Router with ZeroMQ")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
