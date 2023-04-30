from node_config import *
import networking
import time
import actuation
import command



# probably want some global variables here...
# The previously reported temperature values.
prev_heat = None
prev_cool = None
prev_fan = None
# Timing variables.
LOOP_INTERVAL_NS = 1000000000
_prev_time = time.monotonic_ns()


#-----------network setup-------------------#

# Called when a message is received over the socket
def socket_message_received(msg):
    # Parse the message as a Command
    cmd = command.Command(msg=msg)
    print(f'Command received: {cmd}, values: {cmd.values}')

    if mode == AUTOMATIC_MODE:
        if cmd.type == command.TYPE_HEAT_COOL:
            if cmd.values == command.HEAT_COOL_HEATING:
                actuation.set_heating(True)
                return

            if cmd.values == command.HEAT_COOL_COOLING:
                actuation.set_cooling(True)
                return
            
            if cmd.values == command.HEAT_COOL_OFF:
                actuation.set_heating(False)
                actuation.set_cooling(False)
                return


# Called when an MQTT message is received.
# topic is the feed name the message was published on.
# message is the contents of the message.
def message_received_sec(client, topic, message):
    print(f"New message on topic {topic}: {message}")
    # TODO: Parse the feed name and take action

    if mode == MANUAL_MODE:
        if topic==networking.SETHEATING_FEED:
            actuation.set_heating(int(message))
            return

        if topic==networking.SETCOOLING_FEED:
            actuation.set_cooling(int(message))
            return
        
        if topic==networking.SETFAN_FEED:
            actuation.set_circulating(int(message))
            return

# TODO: set up networking, subscribe to feeds, and send initial feed messages
# Set up networking.
networking.connect_to_network()
networking.mqtt_initialize()
networking.mqtt_connect([networking.HEATING_FEED, networking.COOLING_FEED, networking.FAN_FEED, networking.SETHEATING_FEED, networking.SETCOOLING_FEED, networking.SETFAN_FEED ], message_received_sec)
networking.mqtt_connect([networking.SECONDARY_NODE], socket_message_received)
# networking.connect_to_network()
# networking.socket_connect()     for sockets

#-----------network setup-------------------#


#publishes damper, heater and cooler messages to the AIO
def publish_messages_sec():
    global prev_cool, prev_heat

    # publish heating message
    if prev_heat==None or prev_heat != actuation.get_heater():
        networking.mqtt_publish_message(networking.HEATING_FEED, str(actuation.get_heater()))
        prev_heat = actuation.get_heater()

    # publish cooling message
    if prev_cool==None or prev_cool != actuation.get_cooler():
        networking.mqtt_publish_message(networking.COOLING_FEED, str(actuation.get_cooler()))
        prev_cool = actuation.get_cooler()

    # publish fan message
    if prev_fan==None or prev_fan != actuation.get_fan():
        networking.mqtt_publish_message(networking.FAN_FEED, str(actuation.get_fan()))
        prev_fan = actuation.get_fan()


# Perform regular secondary node control tasks
def loop():
    # Only run this code if LOOP_INTERVAL_NS have elapsed.
    global _prev_time
    curr_time = time.monotonic_ns()
    if curr_time - _prev_time < LOOP_INTERVAL_NS:
        return
    _prev_time = curr_time

    publish_messages_sec()







