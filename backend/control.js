/* 
General Schema
    name: str,
    currentEnergyUse: int/float?
    maxEnergyUse: int/float?
    control function: function
    priority = value;

Updating relevant values every timestep

Assumptions: Make it AS ~PEAKY~ AS POSSIBLE
    Winter
    Cold place
*/

// Appliance class
class Appliance {
  constructor(applianceName, maxEnergyUse, priority) {
    applianceName = applianceName;
    currentEnergyUse = maxEnergyUse;
    maxEnergyUse = maxEnergyUse;
    priority = priority;
  }
}

// EV charger
class EvCharger extends Appliance {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
    /* 
          other needed attributes:
          startingChargeTime
          endingChargeTime
          currentBatteryPercentage
        */
  }

  control() {}
}

// heat-pump HVAC (air-source?)
class HeatPump {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
    /* 
          other needed attributes:
          insideTemperature
          outsideTemperature (factor in later)
        */
  }

  control() {}
}

// Probably not shiftable, high priority when it is on
// induction range/oven
class Oven {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
    /* 
          other needed attributes:
          none
        */
  }

  control() {}
}

// lighting, miscellaneous
// Also dispatchable?? dim lights??
// brightness == currentEnergyUse/maxEnergyUse
// Priority based on room??
class Lighting {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
    /* 
          other needed attributes:
          none
        */
  }

  control() {}
}

// heat-pump water heater
class WaterHeater {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
    /* 
          other needed attributes:
          tankCapacity
          hotWaterInTank
          maxWaterForTime
        */
  }

  control() {}
}

// washer/dryer
class WasherDryer {
  constructor(applianceName, maxEnergyUse) {
    super(applianceName, maxEnergyUse);
  }

  control() {}
}
