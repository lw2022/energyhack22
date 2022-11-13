import numpy as np


class Appliance:
  def __init__(self, applianceName, maxEnergyUse, priority):
    self.applianceName = applianceName
    self.currentEnergyUse = maxEnergyUse
    self.maxEnergyUse = maxEnergyUse
    self.priority = priority
    
    return


class EvCharger(Appliance):
  def __init__(self, applianceName, maxEnergyUse, priority):
    super().__init__(applianceName, maxEnergyUse, priority)

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

# Environmental variable functions
# Returns inside temperature
def getInsideTemp():
    # In this situation, calculate inside temperature based on outside temperature and activity of heat pump
    # Assume we have it because IRL you would just be able to measure this, too many environmental factors
    return 60

# Outside temps based on temps for 1/30/22 https://www.timeanddate.com/weather/usa/boston/historic?month=1&year=2022
# Returns linear approximation of outside temperature
def getOutsideTemp(minute):
    if minute < 360: 
        return 12
    elif minute < 720:
        return (7/360)*(minute-360) + 12
    elif minute < 900:
        return (4/180)*(minute-720) + 19
    elif minute < 1080:
        return -(4/180)*(minute-900) + 23
    else:
        return -(1/360)*(minute-1080) + 19

# Returns "predicted" water usage
def getWaterUsage():
    # Calculate based on demand curve
    return 0.1


from os.path import exists
from pyomo.environ import *
from pyomo.environ import *
from pyomo.dae import *

class Controller():
  def __init__(self):

    self._dt = 1    # timestep of 1 min
    self._horizon = 10  # horizon 

    return 
  
  def optimization(self, priorities, appliances):
    """
    MPC framework for optimizing power output. MILP formulation
    Runs at certain point in time - requires initial condition inputs
    Calls appliances to get energy usage and constants?

    priorities - horizon x appliances? or should this be stored in each appliance
    
    """

    stateVars = []
    actionVars = []
    appList = []
    # state and action variables
    for app in appliances:
      for t in range(0, self._horizon-1, self._dt):
        stateVars.append((app.applianceName, t, 'state'))
        actionVars.append((app.applianceName, t, 'action'))

        appList.append(app.applianceName)
      stateVars.append((app.applianceName, self._horizon-1, 'state'))


    m = ConcreteModel()
    m.bounds = ConstraintList()
    for appName in appList:
      if appName=='EvCharger':
        vars = [var for var in stateVars if var[0]==appName]
        m.varsEvState = Set(initialize=vars)
        m.EvChargerState = Var(m.varsEvState)

        vars = [var for var in actionVars if var[0]==appName]
        m.varsEvAction = Set(initialize=vars)
        m.EvChargerAction = Var(m.varsEvAction)

        for t in range(0, self._horizon-1, self._dt):
          m.bounds.add(m.varsEvAction['EvCharger', t, 'action'] <= 5)
          m.bounds.add(m.varsEvAction['EvCharger', t, 'action'] >= 0)
    # m.
    # m.vars = Set(initialize = vars)
    # m.w = Var(m.vars, domain=Binary)    # indexing is (id, q, r, s, time, layer)

    # time evolution
    m.sim = ConstraintList()
    
    for i in range(0, self._horizon-1, self._dt):
      # EV simulation
      m.sim.add(m.varsEvState['EvCharger', t+1, 'state'] == m.varsEvState['EvCharger', t, 'action'] + chargeCoeff * m.varsEvAction['EvCharger', t, 'action'] * self._dt)
      



    print(m.pprint())

    return
