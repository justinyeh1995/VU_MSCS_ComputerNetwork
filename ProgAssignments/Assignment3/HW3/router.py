# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use DEALER-ROUTER sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# This code is for the intermediate router.
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)

# import the needed packages
import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import zmq    # this package must be imported for ZMQ to work
import re
import subprocess
import pandas as pd
import configparser # for configuration parsing

testDB = pd.read_csv("./RouteDB_12.csv")
ip2host = {f"10.0.0.{i}": f"H{i}" for i in range(1,30)}
host2ip = { f"H{i}": f"10.0.0.{i}" for i in range(1,30)}
##################################
# Driver program
##################################
def driver (args):

  # Now, get the configuration object
  config = configparser.ConfigParser ()
  config.read (args.config)

  # initialize the config object
  if config["TCP"]["DB"] == "12":
    DB = pd.read_csv("./RouteDB_12.csv")
  else:
    DB = pd.read_csv("./RouteDB_3.csv")
    
  #######################
  ## Intinalize Router ##
  #######################
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
  #################
  ## Bind Socket ##
  #################
  try:
    # as in a traditional socket, tell the system what port are we going to listen on
    # Moreover, tell it which protocol we are going to use, and which network
    # interface we are going to listen for incoming requests. This is TCP.
    print ("Bind the ROUTER socket")
    ifconfig_output=(subprocess.check_output('ifconfig')).decode()
    regex_ip=re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",ifconfig_output)
    my_ip = str(regex_ip.group(0))
    print(f"Router Host HostName is {ip2host[my_ip]}")
    bind_string = "tcp://" + my_ip + ":" + str (args.myport)
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
  ##########################
  ## Register bind socket ##
  ##########################
  try:
    # register sockets
    print ("Register sockets for incoming events")
    poller.register (bind_sock, zmq.POLLIN)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error registering with poller: {}".format (err))
    return
  except:
    print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
    return
  
  ##################################################################
  ## Additional data structure for handing duplicate registration ##
  ##################################################################
  connected = set()
  conn_sock_pool = dict()
  ##################################
  ## Forwarding incoming requests ##
  ##################################
  # since we are a server, we service incoming clients forever
  print ("Router now starting its forwarding loop")
  while True:
    try:
      # collect all the sockets that are enabled in this iteration
      print ("Poller polling at binding phase")
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
        print ("Receive from prev hop")
        request = bind_sock.recv_multipart ()
        print("Router received request from prev hop via ROUTER: %s" % request)
        print(request[-3])
        final_dest = request[-3].decode("utf-8").split(":")[0]
        print(final_dest)
        ###################
        ## Table Look Up ##
        ###################
        print("Consulting the Routing Table...")
        try:
          ## Get host ip & convert it to host name
          print("Obtaining the Next Hop Host Name")
          nexthost = DB.loc[DB.host==ip2host[my_ip]].loc[DB.destination==final_dest].nexthop.values[0] # replace "10.0.0.5" with final destination
          nexthop = host2ip[nexthost]
          print(f"Next Router HostName is {nexthost}")
          print(f"Next Router Host IP is {nexthop}")
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
      ###############################################
      ## Try to avoid duplicate registrations here ##
      ###############################################
      if final_dest in connected:
        conn_sock = conn_sock_pool[final_dest]
      else:
        try:
          print ("Router acquiring connection socket")
          conn_sock = context.socket (zmq.DEALER)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error obtaining context: {}".format (err))
          return
        except:
          print ("Some exception occurred getting DEALER socket {}".format (sys.exc_info()[0]))
          return
        ##############################
        ## Add identity for look up ##
        ##############################
        try:
          # set our identity
          print ("router setting its identity: {}".format (ip2host[my_ip]))
          conn_sock.setsockopt (zmq.IDENTITY, bytes (ip2host[my_ip], "utf-8"))
        except zmq.ZMQError as err:
          print ("ZeroMQ Error setting sockopt: {}".format (err))
          return
        except:
          print ("Some exception occurred setting sockopt on REQ socket {}".format (sys.exc_info()[0]))
          return
        ################################
        ## connect socket to next hop ##
        ################################
        try:
          # as in a traditional socket, tell the system what IP addr and port are we
          # going to connect to. Here, we are using TCP sockets.
          print ("Router connecting to next hop")
          nexthopport = 4444
          if nexthost in ["H5", "H6"]:
              nexthopport = 5555
          connect_string = "tcp://" + nexthop + ":" + str (nexthopport)
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
        ##############################
        ## Register this connection ##
        ##############################
        try:
          # register sockets
          print ("Register sockets for incoming events")
          poller.register (conn_sock, zmq.POLLIN)
        except zmq.ZMQError as err:
          print ("ZeroMQ Error registering with poller: {}".format (err))
          return
        except:
          print ("Some exception occurred getting poller {}".format (sys.exc_info()[0]))
          return
        ##############################
        ## remember this connection ##
        ##############################
        conn_sock_pool[final_dest] = conn_sock
        connected.add(final_dest)

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

    ###########################
    ## Handle DEALER socket  ##
    ###########################
    try:
      # collect all the sockets that are enabled in this iteration
      print ("Poller polling at connecting phase")
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
        print ("Receive from next hop")
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


##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
  parser.add_argument ("-a", "--myaddr", default="*", help="Interface to bind to (default: *)")
  parser.add_argument ("-p", "--myport", type=int, default=4444, help="Port to bind to (default: 4444)")
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
