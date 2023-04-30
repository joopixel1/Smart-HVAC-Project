from node_config import *
import networking
import time
import actuation
import command
import sensing



# probably want some global variables here...
# The previously reported damper values values.
prev_damps = [None] * num_zones
prev_instruct = None
# Timing variables.
LOOP_INTERVAL_NS = 1000000000
_prev_time = time.monotonic_ns()

#setPoint
TEMPERATURE_SETPOINT = 22
SETTEMP_FEEDS = []


# Called when an MQTT message is received.
# topic is the feed name the message was published on.
# message is the contents of the message.
def message_received(client, topic, message):
    print(f"New message on topic {topic}: {message}")
    # TODO: Parse the feed name and take action

    if topic == networking.CONTROL:
        mode = int(message)
        return
    
    for i in range(num_zones):
        if topic == networking.SETTEMP_FEEDS[i+1]:
            room_temp[i] = int(message)
            return


    if mode == MANUAL_MODE:
        for i in range(num_zones):
            if topic == networking.SETDAMPER_FEEDS[i+1]:
                actuation.set_damper(int(message))
                return



# TODO: set up networking, subscribe to feeds, and send initial feed messages
# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect(networking.DAMPER_FEEDS+networking.SETDAMPER_FEEDS+networking.SETTEMP_FEEDS+[networking.CONTROL, networking.SECONDARY_NODE], message_received)
# networking.connect_to_network()
# networking.socket_connect()     for sockets


#publishes damper, heater and cooler messages to the AIO
def  publish_messages():
    global prev_damps

    # Make a list of zones that with dampers that we are publishing
    zones = [i for i in range(num_zones)]
    for zone in zones:
        current_damp = actuation.get_damper_position(zone)
        print(f'Zone {zone} temp: {current_damp}')

        # do we need to report the temperature EVERY time? Report only if the new reading is
        # significantly different from the old one!
        if prev_damps[zone] == None or current_damp > (prev_damps[zone]+2):
            networking.mqtt_publish_message(networking.DAMPER_FEEDS[zone], current_damp)
            prev_damps[zone] = current_damp


# Runs periodic node tasks.
def loop():
    # Only run this code if LOOP_INTERVAL_NS have elapsed.
    global _prev_time
    curr_time = time.monotonic_ns()
    if curr_time - _prev_time < LOOP_INTERVAL_NS:
        return
    _prev_time = curr_time


    if mode == AUTOMATIC_MODE:
        zones = [i for i in range(num_zones)]

        # check if we need to on the heater or cooler
        instruct =command.HEAT_COOL_OFF
        for zone in zones:
            current_temp = sensing.get_current_temperature_f(zone)
            if current_temp < room_temp[zone]-1: 
                instruct = command.HEAT_COOL_HEATING
            elif current_temp > room_temp[zone]+1: 
                instruct = command.HEAT_COOL_COOLING

        if prev_instruct == None or instruct != prev_instruct:
            #send the instruction to secondary node
            networking.mqtt_publish_message(networking.SECONDARY_NODE, instruct)
            prev_instruct = instruct

        if actuation.get_heater() or actuation.get_cooler():
            for zone in zones:
                current_temp = sensing.get_current_temperature_f(zone)
                actuation.set_damper((100 - (current_temp-room_temp[zone])) *100)
        
    elif mode == MANUAL_MODE: 
        pass

    publish_messages()




