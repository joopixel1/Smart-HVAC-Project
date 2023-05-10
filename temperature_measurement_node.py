from node_config import *
import networking
import time
import sensing
# import adafruit_dotstar
# import board


# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect(networking.TEMP_FEEDS)
# networking.socket_connect()     for sockets

# The previously reported temperature values.
prev_temps = [None] * num_zones

# Timing variables.
LOOP_INTERVAL_NS = 1000000000
_prev_time = time.monotonic_ns()



# Runs periodic node tasks.
def loop():
    # Only run this code if LOOP_INTERVAL_NS have elapsed.
    global _prev_time
    curr_time = time.monotonic_ns()
    if curr_time - _prev_time < LOOP_INTERVAL_NS:
        return
    _prev_time = curr_time

    # Make a list of zones that we're reporting temperature for. This allows us to report all
    # zones for a simulated node.
    zones = [zone_id]
    if node_type == NODE_TYPE_SIMULATED:
        zones = [i for i in range(num_zones)]

    for zone in zones:
        current_temp = sensing.get_current_temperature_f(zone)
        print(f'Zone {zone} temp: {current_temp}')

        # TODO: do we need to report the temperature EVERY time? Report only if the new reading is
        # significantly different from the old one!
        if prev_temps[zone] == None or abs(current_temp -prev_temps[zone]) >1:
            networking.mqtt_publish_message(networking.TEMP_FEEDS[zone], current_temp)
            prev_temps[zone] = current_temp
                
        
        #for displaying on an led: red means warm, blue means cold
        # Get the R,G,B values of the next colour
        # r,g,b = dotstar_color_wheel(current_temp*2.55)
        # Set the colour on the dotstar
        # dotstar[0] = ( r, g, b, 0.6)



# Create a DotStar instance
#dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)
#for d dotstar
# def dotstar_color_wheel(wheel_pos):
#     """Color wheel to allow for cycling through the rainbow of RGB colors."""
#     wheel_pos = wheel_pos % 255

#     if wheel_pos < 85:
#         return 255 - wheel_pos * 3, 0, wheel_pos * 3
#     elif wheel_pos < 170:
#         wheel_pos -= 85
#         return 0, wheel_pos * 3, 255 - wheel_pos * 3
#     else:
#         wheel_pos -= 170
#         return wheel_pos * 3, 255 - wheel_pos * 3, 0