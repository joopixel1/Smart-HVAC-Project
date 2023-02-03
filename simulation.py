from node_config import num_zones
import time
from zone import Zone

# TODO: define some values?


# The Simulation(R)
_sim = None

# We only want ONE Simulation object, and we want to share it between all of the modules. We can accomplish this
# using the singleton design pattern. This function is a key part of that pattern. It returns the singleton instance.
# Call "simulation.get_instance()" to get a Simulation, instead of instantiating a Simulation directly.
def get_instance():
    global _sim
    if _sim is None:
        _sim = Simulation(num_zones)
    return _sim

# A class that simulates the physical environment for the system.
class Simulation:
    # Initializes the simulation.
    def __init__(self, num_zones):
       # TODO: initialize additional class variables. These are probably variables that represent the state of the physical system.
       self.zones=[]
       for i in range(num_zones):
            newzone = Zone()
            self.zones.append(newzone)
       #self.num_zones = num_zones
       self.heating = False
       self.cooling = False

    # Returns the current temperature in the zone specified by zone_id
    def get_temperature_f(self, zone_id):
        # TODO: implement
        
        return self.zones[zone_id].getTemp()

    # Sets the damper(s) for the zone specified by zone_id to the percentage
    # specified by percent. 0 is closed, 100 is fully open.
    def set_damper(self, zone_id, percent):
        # TODO: implement
        self.zones[zone_id].setDamper(percent)

    # Update the temperatures of the zones, given that elapsed_time_ms milliseconds
    # have elapsed since this was previously called.
    def _update_temps(self, elapsed_time_ms):
        # TODO: Update all temps
        for i in range (num_zones):
            self.zones[i].updateTemp(elapsed_time_ms)
        pass
    
    # Runs periodic simulation actions.
    def loop(self):
        # TODO: Calculate the amount of time elapsed since this last time this function was run. See CircuitPython's time module documentation
        # at http://docs.circuitpython.org/en/latest/shared-bindings/time/index.html. We recommend time.monotonic_ns(). Also note that
        # temperature_measurement_node.py has an elapsed time calculation, and you may be able to use a similar approach here.
        
        # TODO: pass in the actual elapsed time.
        self._update_temps(0)

# Used for testing the simulation.
if __name__ == '__main__':
    sim = get_instance()

    while True:
        sim.loop()
        time.sleep(1)

        for zone in range(num_zones):
            temp = sim.get_temperature_f(zone)
            print(f'Zone {zone} temp: {temp}')

        # TODO: add additional testing code, e.g. what happens if you turn on heating/cooling?