from node_config import *
import networking
import time

# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect()

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
        # TODO: Get the current temperature using the appropriate function from the sensing module
        current_temp = 0

        # TODO: Also consider printing it!

        # TODO: do we need to report the temperature EVERY time? Report only if the new reading is
        # significantly different from the old one!
        networking.mqtt_publish_message(networking.TEMP_FEEDS[zone], current_temp)