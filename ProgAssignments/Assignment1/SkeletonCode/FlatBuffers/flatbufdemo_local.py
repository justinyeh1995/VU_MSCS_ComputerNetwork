#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  Modified: Fall 2022 (for Computer Networking course)
#
#  Purpose: demonstrate serialization of a user-defined data structure using
#  FlatBuffers
#
#  Here our custom message format comprises a sequence number, a timestamp, a name,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us) 

# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

## the following are our files
from custom_msg import CustomMessage  # our custom message in native format
from custom_msg_local import GroceryOrderMessage, HealthStatusMessage, ResponseMessage
import serialize as sz  # this is from the file serialize.py in the same directory

##################################
#        Driver program
##################################

def driver (name, iters, vec_len):

  print ("Driver program: Name = {}, Num Iters = {}, Vector len = {}".format (name, iters, vec_len))
    
  for i in range (iters):
    print ("-----Iteration: {} contents of message before serializing ----------".format (i))
    if i % 2 == 0:    
      ## for every iteration, let us fill up our custom message with some info
      #cm.seq_num = i # this will be our sequence number
      #cm.ts = time.time ()  # current time
      #cm.name = name # assigned name
      #cm.vec = [random.randint (1, 1000) for j in range (vec_len)]
      #print ("-----Iteration: {} contents of message before serializing ----------".format (i))
      #cm.dump ()
      cm = GroceryOrderMessage ()   # create this once and reuse it for send/receive
      cm.type = "ORDER"
      content = {
                "veggies": 
                { 
                    "tomato": round(random.uniform(33.33, 66.66), 2),
                    "cucumber": round(random.uniform(33.33, 66.66), 2), 
                    "potato": round(random.uniform(33.33, 66.66), 2), 
                    "bokchoy": round(random.uniform(33.33, 66.66), 2), 
                    "broccoli": round(random.uniform(33.33, 66.66), 2) 
                }, 
                "drinks": 
                {
                    "cans": 
                    {
                        "coke": random.randint(1,5),
                        "beer": random.randint(1,5),
                        "soda": random.randint(1,5)
                    },
                    "bottles": 
                    {
                        "Sprite": random.randint(1,5),
                        "Gingerale": random.randint(1,5),
                        "SevenUp": random.randint(1,5)
                    }
                }, 
                "milk": [(random.randint(1,6), round(random.uniform(33.33, 66.66), 2)) for i in range(random.randint(1,5))], 
                "bread": [(random.randint(1,3), round(random.uniform(33.33, 66.66), 2)) for i in range(random.randint(1,5))], 
                "meat": [(random.randint(1,4), round(random.uniform(33.33, 66.66), 2)) for i in range(random.randint(1,5))]
                }
      cm.addContent(content) # this line is required it will translate the message above to a full message.

    else:
      cm = HealthStatusMessage()
      cm.type = "HEALTH"
      status = [random.randint(1,3), random.randint(1,100), random.randint(1,2), random.randint(1,100), random.randint(1,100), random.randint(1,2)]
      cm.addContent(status)
    
    print ("-----Iteration: {} contents of message before serializing ----------".format (i))
    cm.__str__()
        
    # here we are calling our serialize method passing it
    # the iteration number, the topic identifier, and length.
    # The underlying method creates some dummy data, fills
    # up the data structure and serializes it into the buffer
    print ("serialize the message")
    start_time = time.time ()
    buf = sz.serialize (cm)
    end_time = time.time ()
    print ("Serialization took {} secs".format (end_time-start_time))

    # now deserialize and see if it is printing the right thing
    print ("deserialize the message")
    start_time = time.time ()
    cm = sz.deserialize (buf)
    end_time = time.time ()
    print ("Deserialization took {} secs".format (end_time-start_time))

    print ("------ contents of message after deserializing ----------")
    cm.__str__ ()

    # sleep a while before we send the next serialization so it is not
    # extremely fast
    time.sleep (0.050)  # 50 msec


##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
    parser.add_argument ("-l", "--veclen", type=int, default=20, help="Length of the vector field (default: 20; contents are irrelevant)")
    parser.add_argument ("-n", "--name", default="FlatBuffer Local Demo", help="Name to include in each message")
    # parse the args
    args = parser.parse_args ()

    return args
    
#------------------------------------------
# main function
def main ():
    """ Main program """

    print("Demo program for Flatbuffer serialization/deserialization")

    # first parse the command line args
    parsed_args = parseCmdLineArgs ()
    
   # start the driver code
    driver (parsed_args.name, parsed_args.iters, parsed_args.veclen)

#----------------------------------------------
if __name__ == '__main__':
    main ()
