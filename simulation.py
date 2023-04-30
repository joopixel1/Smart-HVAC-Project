from node_config import num_zones
import time
from zone import Zone

#  define some constants
LOOP_INTERVAL_NS = 1000000000


# The Simulation(R)
_sim = None
# We only want ONE Simulation object, and we want to share it between all of the modules. We can accomplish this
# using the singleton design pattern. This function is a key part of that pattern. It returns the singleton instance.
# Call "simulation.get_instance()" to get a Simulation, instead of instantiating a Simulation directly.
def get_instance():
    global _sim
    if _sim is None:
        _sim = Simulation()
    return _sim


# A class that simulates the physical environment for the system.
class Simulation:
    
    
    # Initializes the simulation.
    def __init__(self):
       self.zones=[]
       for i in range(num_zones):
            newzone = Zone(self)
            self.zones.append(newzone)
       #True means heat, cold is cool 
       self.heat = False 
       self.cool = False
       self.fan = False
       self.prev_time = time.monotonic_ns()
       self.heaterMaxTemp = 100
       self.coolerMaxTemp = 0


    # Returns the current temperature in the zone specified by zone_id
    def get_temperature_f(self, zone_id):        
        return self.zones[zone_id].getTemp()

    # Sets the damper(s) for the zone specified by zone_id to the percentage
    # specified by percent. 0 is closed, 100 is fully open.
    def set_damper(self, zone_id, percent):
        self.zones[zone_id].setDamper(percent)

     # Returns the current damper pos in the zone specified by zone_id
    def get_damper_pos(self, zone_id):        
        return self.zones[zone_id].getDamper()        


    # Update the temperatures of the zones, given that elapsed_time_ms milliseconds
    # have elapsed since this was previously called.
    def _update_temps(self, elapsed_time_ms):
        if elapsed_time_ms >= LOOP_INTERVAL_NS:
            for i in range (num_zones):
                self.zones[i].updateTemp()
            self.prev_time = time.monotonic_ns()
    
    
    # Runs periodic simulation actions.
    def loop(self):
        # Calculate the amount of time elapsed since this last time this function was run. See CircuitPython's time module documentation
        # at http://docs.circuitpython.org/en/latest/shared-bindings/time/index.html. We recommend time.monotonic_ns(). Also note that
        # temperature_measurement_node.py has an elapsed time calculation, and you may be able to use a similar approach here.
        curr_time = time.monotonic_ns()
        self._update_temps(curr_time - self.prev_time)



# Used for testing the simulation.
if __name__ == '__main__':
    sim = get_instance()
    #now, j = time.monotonic_ns(), 0
    #now, j = time.monotonic_ns(), 0
    
    while True:
        sim.loop()
        time.sleep(1)

        for zone in range(num_zones):
            temp = sim.get_temperature_f(zone)
            print(f'Zone {zone} temp: {temp}')

        # TODO: add additional testing code, e.g. what happens if you turn on heating/cooling?
        if sim.heaterTemp-1 <= temp and sim.heat_cool :
            sim.heat = True
            sim.cool = False
        if sim.coolerTemp+1  >= temp and not sim.heat_cool:
            sim.cool = True
            sim.heat = False