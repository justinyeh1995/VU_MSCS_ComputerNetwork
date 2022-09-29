# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the definition of supported messages
# Purpose: Define a native representation of a custom message format
#          that will then undergo serialization/deserialization
#

# import the needed packages
import sys
from enum import Enum  # for enumerated types
# @TODO import whatever more packages are needed
from typing import List, Dict
from dataclasses import dataclass

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

'''
  type: str
  contents:

    veggies:

        tomato: <floating point value in pounds>

        cucumber: <floating point value in pounds>

        potato: <floating point value in pounds>

        bok choy: <floating point value in pounds>

        broccoli: <floating point value in pounds>

    drinks:

        cans: /* assume pack of 6 */
            coke: <integer quantity representing number of packs>
            beer: <integer quantity representing number of packs>
            soda: <integer quantity representing number of packs>

        bottles:

            sprite: <integer representing number of bottles>
            Gingerale: <integer representing number of bottles>
            SevenUp: <integer representing number of bottles>

    milk: /* will be an array/list of 2 tuples as shown */

        [{type: <an enumerated type>, quantity: <floating point in gallons>}+]

        /* the + above is regular expression operator meaning 1 or more */

        /* Create an enumeration for type, which can be 1%, 2%, fat free, whole, almond, cashew, oat */

    bread:

        [I urge you to do something similar like we do for milk with bread types, e.g. whole wheat, pumpernickel, rye, etc]

    meat:

        [I urge you to do something similar like we do for milk but here for meat types]
    
'''
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
#  Subclasses for GroceryMessage
############################################
@dataclass
class Cans:
  coke: int
  beer: int
  soda: int

@dataclass
class Bottles:
  Sprite: int
  Gingerale: int
  SevenUp: int

@dataclass
class Container:
  cans: Cans
  bottles: Bottles
  
  def __init__(self):
    pass

  def addCans(self, can):
    self.cans = Cans(**can).__dict__
  def addBottles(self, bottle):
    self.bottles = Bottles(**bottle).__dict__
    
@dataclass
class Veggies:
  tomato: float
  cucumber: float  
  potato: float
  bokchoy:float  
  broccoli: float

class MilkType(Enum):
  ONE_PCT = 1
  TWO_PCT = 2
  FAT_FREE = 3
  WHOLE = 4
  CASHEW = 5
  OAT = 6 

@dataclass
class Milk:
  type: MilkType
  quantity: float

class BreadType(Enum):
  WHOLE_WEAT = 1
  PUMPERNICKEL = 2
  RYE = 3

@dataclass
class Bread:
  type: BreadType
  quantity: float

class MeatType(Enum):
  PORK = 1
  LAMB = 2
  CHICKEN = 3
  BEEF = 4

@dataclass
class Meat:
  type: str
  quantity: float

@dataclass
class Grocery:
  veggies: Veggies 
  drinks: Container
  milk: List[Dict]
  bread: List[Dict]
  meat: List[Dict]    
  
  def __init__(self):
    pass

  def addVeggies(self, veg):
    self.veggies = Veggies(**veg).__dict__
    return self.veggies
  
  def addDrinks(self, drink):
    c = Container()
    c.addCans(drink["cans"])
    c.addBottles(drink["bottles"])
    self.drinks = c.__dict__
  
  def addMilk(self, details):
    self.milk = [Milk(MilkType(i).name, n).__dict__ for i,n in details]

  def addBread(self, details):
    self.bread = [Bread(BreadType(i).name, n).__dict__ for i,n in details]
    
  def addMeat(self, details):
    self.meat = [Meat(MeatType(i).name, n).__dict__ for i,n in details]

@dataclass
class GroceryOrderMessage:
  """ Our message in native representation"""
    # @TODO - the above is simply to test the code. You need to get rid of that dummy
    # and replace it with the complex data struture we have for the health status
    # as represented in the host (as a Python language data structure)

  type: str
  contents: Dict #= field(default_factory=Grocery)
  
  def __init__ (self):
    pass

  def addContent(self, order):
    g = Grocery()
    g.addVeggies(order["veggies"])
    g.addDrinks(order["drinks"])
    g.addMilk(order["milk"])
    g.addBread(order["bread"])
    g.addMeat(order["meat"])
    self.contents = g.__dict__
  
  def __str__(self):
    print (f"Dumping contents of {self.type} Message")
    print (f"\tContents:  ")
    print (f"\t\tveggies:")
    for key in self.contents["veggies"]:
        print (f"\t\t\t{key}: {self.contents['veggies'][key]}")
    print (f"\t\tdrinks:")
    for container in self.contents["drinks"]:
        print (f"\t\t\t{container}:")
        for key in self.contents["drinks"][container]:
            print (f"\t\t\t\t{key}: {self.contents['drinks'][container][key]}")
    print (f"\t\tmilk:")
    print (f"\t\t\t{self.contents['milk']}")
    print (f"\t\tbread:")
    print (f"\t\t\t{self.contents['bread']}")
    print (f"\t\tmeat:")
    print (f"\t\t\t{self.contents['meat']}")
    return "Groceries..." 

############################################
#  Health Status Message
############################################
'''
type: HEALTH

contents:

    dispenser: /* decide an enumeration like OPTIMAL, PARTIAL, BLOCKAGE */

    icemaker: <integer reflecting the percentage efficiency it is working at>

    lightbulb: <GOOD or BAD (i.e., not working)>

    fridge_temp: <integer representing internal temp>

    freezer_temp: <integer representing internal temp, could be negative>

    sensor_status: /* some enumeration like GOOD or BAD */

    /* use your imagination and add maybe another field or two */
'''
class Decision(Enum):
  OPTIMAL = 1
  PARTIAL = 2
  BLOCKAGE = 3

class Status(Enum):
  GOOD = 1
  BAD = 2

@dataclass
class HealthStatus:  
  dispenser: str
  icemaker: int
  lightbulb: str
  fridge_temp = int
  freezer_temp = int
  sensor_status: str

  def __init__ (self):
    pass
  
  def addDispenser(self, index):
    self.dispenser = Decision(index).name

  def addBulbStatus(self, index):
    self.lightbulb = Status(index).name

  def addSensorStatus(self, index):
    self.sensor = Status(index).name
    
@dataclass
class HealthStatusMessage:
  '''Health Status Message'''
    # @TODO - the above is simply to test the code. You need to get rid of that dummy
    # and replace it with the complex data struture we have for the health status
    # as represented in the host (as a Python language data structure)

  type: str
  contents: Dict 
  
  def __init__ (self):
    pass

  def addContent(self, status):
    h = HealthStatus()
    h.addDispenser(status[0]) # 1~3
    h.icemaker = status[1]
    h.addBulbStatus(status[2]) # 1~2
    h.fridge_temp = status[3]
    h.freezer_temp = status[4]
    h.addSensorStatus(status[5]) # 1~2
    self.contents = h.__dict__

  def __str__ (self):
    '''Pretty print the contents of the message'''
    print (f"Dumping contents of {self.type} Message")
    print (f"\tContents: ")
    for key in self.contents:
        print (f"\t\t{key}: {self.contents[key]}")
    return "Health Status..." 
############################################
#  Response Message
############################################
'''
code: /* enumeration indicating OK or BAD_REQUEST */

contents: /* “Order Placed”, or “You are Healthy” or “Bad Request” */
'''
class reqStatus(Enum):
   OK = 1
   BAD_REQUEST = 2

@dataclass
class ResponseMessage:
  '''Response Message'''
  # @TODO - the above is simply to test the code. You need to get rid of that dummy
  # and replace it with the data struture we have for the response message 
  # as represented in the host (as a Python language data structure)
  type: str
  code: str
  contents: str
  
  def __init__(self):
    pass

  def addCode(self,index):
    self.code = reqStatus(index).name

  def __str__ (self):
    '''Pretty print the contents of the message'''

    #@TODO - remove the above print stmt and instead create a pretty print logic
    for key in self.__dict__:
        print(f"{key}: {self.__dict__.get(key)}")    
    return "Response..." 

