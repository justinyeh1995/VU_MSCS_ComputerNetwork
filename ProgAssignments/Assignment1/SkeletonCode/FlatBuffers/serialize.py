#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/gokhale/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field

import zmq   # we need this for additional constraints provided by the zmq serialization

from custom_msg import CustomMessage  # our custom message in native format
from custom_msg_local import GroceryOrderMessage, HealthStatusMessage, ResponseMessage # used in deserialization here
import CustomAppProto.Message as msg   # this is the generated code by the flatc compiler

import Proto.HealthStatusProto.Message as health   # this is the generated code by the flatc compiler
import Proto.HealthStatusProto.Contents as contents   # this is the generated code by the flatc compiler
import Proto.HealthStatusProto.Decision as decision
import Proto.HealthStatusProto.Status as status

import Proto.GroceryOrderProto.Message as order   # this is the generated code by the flatc compiler
import Proto.GroceryOrderProto.Bottles as bottles
import Proto.GroceryOrderProto.Cans as cans
import Proto.GroceryOrderProto.Container as container
import Proto.GroceryOrderProto.Veggies as veggies
import Proto.GroceryOrderProto.Milk as milk
import Proto.GroceryOrderProto.MilkType as milktype
import Proto.GroceryOrderProto.Bread as bread
import Proto.GroceryOrderProto.BreadType as breadtype
import Proto.GroceryOrderProto.Meat as meat
import Proto.GroceryOrderProto.MeatType as meattype
import Proto.GroceryOrderProto.Grocery as grocery

import Proto.ResponseProto.Message as res
import Proto.ResponseProto.reqStatus as reqstatus
#
import CustomAppProto.Message as msg   # this is the generated code by the flatc compiler
from custom_msg_local import GroceryOrderMessage, HealthStatusMessage, ResponseMessage

# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.
def serialize (cm):
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    
    builder = flatbuffers.Builder (0);

    # create the name string for the name field using
    # the parameter we passed
    #name_field = builder.CreateString (cm.name)
    # build it bottom up
    
    type_ = builder.CreateString (cm.type)

    if cm.type == "ORDER":
       # create logic for native msg -> flatbuffer msg
        # @TODO@
        #grocery.Start(builder)

        #Bottles = bottles.CreateBottles(builder,cm.contents["drinks"]["bottles"]["Sprite"],
        #                                      cm.contents["drinks"]["bottles"]["Gingerale"],
        #                                      cm.contents["drinks"]["bottles"]["SevenUp"]
        #                                      )
        #Cans = cans.CreateCans(builder,cm.contents["drinks"]["cans"]["coke"],
        #                               cm.contents["drinks"]["cans"]["beer"],
        #                               cm.contents["drinks"]["cans"]["soda"]
        #                               )
        ##Drinks = drinks.CreateDrinks(builder,Cans,Bottles)
        #Drinks = container.CreateContainer(builder,cm.contents["drinks"]["cans"]["coke"],
        #                                           cm.contents["drinks"]["cans"]["beer"],
        #                                           cm.contents["drinks"]["cans"]["soda"],
        #                                           cm.contents["drinks"]["bottles"]["Sprite"],
        #                                           cm.contents["drinks"]["bottles"]["Gingerale"],
        #                                           cm.contents["drinks"]["bottles"]["SevenUp"]
        #                                          )
        #Veggies = veggies.CreateVeggies(builder, cm.contents["veggies"]["tomato"], 
        #                                         cm.contents["veggies"]["cucumber"],
        #                                         cm.contents["veggies"]["potato"],
        #                                         cm.contents["veggies"]["bokchoy"],
        #                                         cm.contents["veggies"]["broccoli"]
        #                                         )

        MilkOrder = []
        for item in cm.contents["milk"]:
            if item["type"] == "ONE_PCT":
                itemtype = milktype.MilkType.ONE_PCT
            elif item["type"] == "TWO_PCT":
                itemtype = milktype.MilkType.TWO_PCT
            elif item["type"] == "FAT_FREE":
                itemtype = milktype.MilkType.FAT_FREE
            elif item["type"] == "WHOLE":
                itemtype = milktype.MilkType.WHOLE
            elif item["type"] == "CASHEW":
                itemtype = milktype.MilkType.CASHEW
            elif item["type"] == "OAT":
                itemtype = milktype.MilkType.OAT
            MilkOrder.append(milk.CreateMilk(builder, itemtype, item["quantity"]))

        grocery.StartMilkVector(builder, len(MilkOrder))
        for i in reversed(range(len(MilkOrder))):
            builder.PrependUOffsetTRelative (MilkOrder[i])
        Milk = builder.EndVector()

        BreadOrder = []
        for item in cm.contents["bread"]:
            if item["type"] == "WHOLE_WEAT":
                itemtype = breadtype.BreadType.WHOLE_WEAT
            elif item["type"] == "PUMPERNICKEL":
                itemtype = breadtype.BreadType.PUMPERNICKEL
            elif item["type"] == "RYE":
                itemtype = breadtype.BreadType.RYE
            BreadOrder.append(bread.CreateBread(builder, itemtype, item["quantity"]))

        grocery.StartBreadVector(builder, len(BreadOrder))
        for i in reversed(range(len(BreadOrder))):
            builder.PrependUOffsetTRelative (BreadOrder[i])
        Bread = builder.EndVector()

        MeatOrder = []
        for item in cm.contents["meat"]:
            if item["type"] == "PORK":
                itemtype = meattype.MeatType.PORK
            elif item["type"] == "LAMB":
                itemtype = meattype.MeatType.LAMB
            elif item["type"] == "CHICKEN":
                itemtype = meattype.MeatType.CHICKEN
            elif item["type"] == "BEEF":
                itemtype = meattype.MeatType.BEEF
            MeatOrder.append(meat.CreateMeat(builder, itemtype, item["quantity"]))
        grocery.StartMeatVector(builder, len(MeatOrder))
        for i in reversed(range(len(MeatOrder))):
            builder.PrependUOffsetTRelative (MeatOrder[i])
        Meat = builder.EndVector()

        grocery.Start(builder)

        grocery.AddVeggies (builder,veggies.CreateVeggies(builder, 
                                                 cm.contents["veggies"]["tomato"], 
                                                 cm.contents["veggies"]["cucumber"],
                                                 cm.contents["veggies"]["potato"],
                                                 cm.contents["veggies"]["bokchoy"],
                                                 cm.contents["veggies"]["broccoli"]
                                                 ))
        grocery.AddDrinks (builder, container.CreateContainer(builder,
                                                   cm.contents["drinks"]["cans"]["coke"],
                                                   cm.contents["drinks"]["cans"]["beer"],
                                                   cm.contents["drinks"]["cans"]["soda"],
                                                   cm.contents["drinks"]["bottles"]["Sprite"],
                                                   cm.contents["drinks"]["bottles"]["Gingerale"],
                                                   cm.contents["drinks"]["bottles"]["SevenUp"]
                                                  ))
        grocery.AddMilk (builder, Milk)
        grocery.AddBread (builder, Bread)
        grocery.AddMeat (builder, Meat)
        
        Grocery = grocery.End(builder)

        order.Start(builder)
        order.AddType (builder, type_)
        order.AddContents (builder, Grocery)
        serialized_msg = order.End(builder)
       
    elif cm.type == "HEALTH":
        health.Start(builder)

        if cm.contents["dispenser"] == "OPTIMAL":
            dispenser = decision.Decision().OPTIMAL    
        elif cm.contents["dispenser"] == "PARTIAL":
            dispenser = decision.Decision().PARTIAL   
        elif cm.contents["dispenser"] == "BLOCKAGE":
            dispenser = decision.Decision().BLOCKAGE    
        
        if cm.contents["lightbulb"] == "GOOD":
            lightbulb = status.Status().GOOD
        else:
            lightbulb = status.Status().BAD
        
        if cm.contents["sensor"] == "GOOD":
            sensorStatus = status.Status().GOOD
        else:
            sensorStatus = status.Status().BAD

        health.AddContents (builder, contents.CreateContents(builder, dispenser, cm.contents["icemaker"], lightbulb, 
            cm.contents["fridge_temp"], cm.contents["freezer_temp"], sensorStatus))
        health.AddType (builder, type_)
        #health.AddContents (builder, ct)
        serialized_msg = health.End (builder)

    elif cm.type == "RESPONSE":
        res.Start(builder)
        # @TODO@
        if cm.code == "OK":
            code = reqstatus.reqStatus().OK    
        elif cm.code == "PARTIAL":
            code = reqstatus.reqStatus().BAD_REQUEST   
        res.AddType (builder, type_)
        res.AddCode (builder, code)
        res.AddContents(builder, cm.contents)
        serialized_msg = res.End(builder)

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  print ("serialize custom message to iterable list")
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize (buf):
    test_packet = health.Message.GetRootAs(buf, 0)
    if test_packet.Type() == b"ORDER":
        cm = GroceryOrderMessage()
        packet = order.Message.GetRootAs(buf, 0)
        cm.type = packet.Type()
        contents = {
                    "veggies": 
                        {"tomato": 0, "cucumber": 0, "potato":0, "bokchoy": 0, "broccoli": 0 },
                    "drinks":
                        {
                            "cans": {
                                "coke": 0,
                                "beer": 0,
                                "soda": 0
                                },
                            "bottles": {
                                "Sprite":0,
                                "Gingerale": 0,
                                "SevenUp": 0
                                }
                            },
                    "milk": [],
                    "bread": [],
                    "meat": []
                }
        contents["veggies"]["tomato"] = packet.Contents().Veggies().Tomato()
        # @TO-DO@
        cm.contents = contents
    elif test_packet.Type() == b"HEALTH":
        cm = HealthStatusMessage()
        packet = health.Message.GetRootAs(buf, 0)
        cm.type = packet.Type()
        contents = {
                "dispenser": "",
                "icemaker": 0,
                "lightbulb": "",
                "fridge_temp":0,
                "freezer_temp": 0,
                "sensor_status": ""
                }
        # @TO-DO@
        cm.contents = contents
    elif test_packet.Type() == b"RESPONSE":
        cm = ResponseMessage()
        packet = order.Message.GetRootAs(buf, 0)
        cm.type = response.Type()
        cm.code = packet.Code()
        cm.contents = packet.Contents()
        # @TO-DO@
    ## sequence number
    #cm.seq_num = packet.SeqNo ()

    ## timestamp received
    #cm.ts = packet.Ts ()

    ## name received
    #cm.name = packet.Name ()

    ## received vector data
    ## We can obtain the vector like this but it changes the
    ## type from List to NumpyArray, which may not be what one wants.
    ##cm.vec = packet.DataAsNumpy ()
    #cm.vec = [packet.Data (j) for j in range (packet.DataLength ())]

    return cm
    
# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  # For this sample code, since we send only one frame, hopefully what
  # comes out is also a single frame. If not some additional complexity will
  # need to be added.
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm
    
