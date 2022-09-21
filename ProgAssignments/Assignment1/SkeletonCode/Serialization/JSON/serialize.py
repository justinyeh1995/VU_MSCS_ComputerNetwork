#  Author: Aniruddha Gokhale
#  Created: Fall 2022
#  (based on code developed for Distributed Systems course in Fall 2019)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using JSON
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

import json # JSON package

from custom_msg import CustomMessage  # our custom message in native format
from custom_msg_local import GroceryOrderMessage, HealthStatusMessage, ResponseMessage

# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize (cm):

  # create a JSON representation from the original data structure
  
  # json_buf = {
  #  "seq_num": cm.seq_num,
  #  "timestamp": cm.ts,
  #  "name": cm.name,
  #  "vector": cm.vec
  #  }
  if cm.type == "ORDER" or cm.type == "HEALTH":
      json_buf = { 
        "type": cm.type,
        "contents": cm.contents
      }
  else:
      json_buf = { "code": cm.code.name, "contents": c.contents }

  # return the underlying jsonified buffer
  return json.dumps(json_buf)

# deserialize the incoming serialized structure into native data type
def deserialize (buf):

  # get the json representation from the incoming buffer
  json_buf = json.loads (buf)

  # now retrieve the native data structure out of it.
  if json_buf["type"] == "ORDER":
      cm = GroceryOrderMessage()
      cm.type = json_buf["type"]
      cm.contents = json_buf["contents"]
  elif json_buf["type"] == "HEALTH":
      cm = HealthStatusMessage()
      cm.type = json_buf["type"]
      cm.contents = json_buf["contents"]
  else:
      cm = ResponseMessage()
      cm.code = json_buf["code"]
      cm.contents = json_buf["contents"]

  return cm
    
    
