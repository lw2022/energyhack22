from control import *

c = Controller()

evcharge = EvCharger('EvCharger', 10, 0.5)
apps = [evcharge]
c.optimization([], apps)