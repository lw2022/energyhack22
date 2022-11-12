import numpy as np


class Appliance:
  def __init__(self, applianceName, maxEnergyUse, priority) :
    applianceName = applianceName
    currentEnergyUse = maxEnergyUse
    maxEnergyUse = maxEnergyUse
    priority = priority
    
    return


class EvCharger(Appliance):
  def __init__(self, applianceName, maxEnergyUse, priority):
    Appliance.__init__(applianceName, maxEnergyUse, priority)

    # other needed attributes:
    # startingChargeTime
    # endingChargeTime
    # currentBatteryPercentage
    return

  def control():
    print("EV control")
    # control fcn


    return NotImplementedError

# heat-pump HVAC (air-source?)
class HeatPump(Appliance): 
  def __init__(self, applianceName, maxEnergyUse, priority):
    Appliance.__init__(applianceName, maxEnergyUse, priority)
        # other needed attributes:
        # insideTemperature
        # outsideTemperature (factor in later)
      
    return

  def control():
      print("Heat pump control")
      
      return NotImplementedError


# Probably not shiftable, high priority when it is on
# induction r
class Oven(Appliance):
    def __init__(self, applianceName, maxEnergyUse, priority):
        Appliance.__init__(applianceName, maxEnergyUse, priority)
            # other needed attributes:
            # none
    
    def control():
        return NotImplementedError


# lighting, miscellaneous
# LED light, brightness is proportional to input 
class Lighting(Appliance):
  def __init__(self, applianceName, maxEnergyUse, priority):
    Appliance.__init__(applianceName, maxEnergyUse, priority)
    # other needed attributes:
      # none

  def control():
    return NotImplementedError


# heat-pump water heater
class WaterHeater(Appliance):
  def __init__(self, applianceName, maxEnergyUse, priority):
    Appliance.__init__(applianceName, maxEnergyUse, priority)
    # other needed attributes:
    # tankCapacity
    # hotWaterInTank
    # maxWaterForTime

  def control():
      return NotImplementedError

# washer/dryer
class WasherDryer(Appliance):
  def __init__(self, applianceName, maxEnergyUse, priority):
    Appliance.__init__(applianceName, maxEnergyUse, priority)

  def control():
      return NotImplementedError


from os.path import exists
from pyomo.environ import *
from pyomo.environ import *
from pyomo.dae import *

class Controller():
  def __init__(self):


    return 
