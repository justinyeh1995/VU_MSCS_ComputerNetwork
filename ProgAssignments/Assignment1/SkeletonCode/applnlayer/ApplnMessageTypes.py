# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the definition of supported messages
#

# import the needed packages
import sys
from enum import Enum  # for enumerated types
# @TODO import whatever more packages are needed

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

############################################
#  Enumeration for Message Types
############################################
class MessageTypes (Enum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  GROCERY = 1
  HEALTH = 2
  RESPONSE = 3

############################################
#  Grocery Order Message
############################################
class GroceryOrderMessage:
  '''Grocery Order Message'''
  def __init__ (self):
    self.dummy = "This is a grocery order message"

    # @TODO - the above is simply to test the code. You need to get rid of that dummy
    # and replace it with the complex data struture we have for the grocery order
    # as represented in the host (as a Python language data structure)

  def __str__ (self):
    '''Pretty print the contents of the message'''
    return self.dummy

    #@TODO - remove the above print stmt and instead create a pretty print logic
    
############################################
#  Health Status Message
############################################
class HealthStatusMessage:
  '''Health Status Message'''
  def __init__ (self):
    self.dummy = "This is a health status message"

    # @TODO - the above is simply to test the code. You need to get rid of that dummy
    # and replace it with the complex data struture we have for the health status
    # as represented in the host (as a Python language data structure)

  def __str__ (self):
    '''Pretty print the contents of the message'''
    return self.dummy

    #@TODO - remove the above print stmt and instead create a pretty print logic
    
############################################
#  Response Message
############################################
class ResponseMessage:
  '''Response Message'''
  def __init__ (self):
    self.dummy = "This is a response message"

    # @TODO - the above is simply to test the code. You need to get rid of that dummy
    # and replace it with the data struture we have for the response message 
    # as represented in the host (as a Python language data structure)

  def __str__ (self):
    '''Pretty print the contents of the message'''
    return self.dummy

    #@TODO - remove the above print stmt and instead create a pretty print logic
    



