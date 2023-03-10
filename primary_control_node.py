# TODO: imports?!
import actuation
import simulation
import time
import sensing

# TODO: probably want some global variables here...

# Called when an MQTT message is received.
# topic is the feed name the message was published on.
# message is the contents of the message.
def message_received(client, topic, message):
    print(f"New message on topic {topic}: {message}")

    # TODO: Parse the feed name and take action

# TODO: set up networking, subscribe to feeds, and send initial feed messages

# Run the regular primary control node tasks
def loop():
    # TODO: throttle this loop? (i.e. don't run it every time)
    
    #print("Executing primary control node loop")
    print(sensing.get_current_temperature_f())
    CurrentTime= time.monotonic_ns()
    throttle = time.monotonic_ns()-CurrentTime
    deltaTime = 300 #make bigger after display
    
#throttle <= deltaTime:
        #cooling
    if sensing.get_current_temperature_f() >= 60: #cooling target
        print(sensing.get_current_temperature_f(), "cooling")
        actuation.set_heating(False)
        throttle = time.monotonic_ns()-CurrentTime
        actuation.set_cooling(True)
    if sensing.get_current_temperature_f() < 10: #heating target
        print(sensing.get_current_temperature_f(), "heating")
        actuation.set_cooling(False)
        throttle = time.monotonic_ns()-CurrentTime
        actuation.set_heating(True)
