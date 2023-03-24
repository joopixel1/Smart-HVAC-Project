# TODO: imports?!
import actuation
import simulation
import time
import sensing

# TODO: probably want some global variables here...
sim = simulation.get_instance()
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
    global CurrentTime
    #print("Executing primary control node loop")
    #print(sensing.get_current_temperature_f())
    
    throttle = time.monotonic_ns()-CurrentTime
    deltaTime = 30000000 #make bigger after display
    
    if throttle >= deltaTime:
        #cooling
        CurrentTime=time.monotonic_ns()
        actuation.set_damper(0, sim.zones[0].damper + 1)
        print(f'Zone {0} temp: {sensing.get_current_temperature_f()} Damper: {sim.zones[0].damper}')


    # if sensing.get_current_temperature_f() >= 60: #cooling target
    #     print(sensing.get_current_temperature_f(), "cooling")
    #     actuation.set_heating(False)
    #     throttle = time.monotonic_ns()-CurrentTime
    #     actuation.set_cooling(True)
    # if sensing.get_current_temperature_f() < 10: #heating target
    #     print(sensing.get_current_temperature_f(), "heating")
    #     actuation.set_cooling(False)
    #     throttle = time.monotonic_ns()-CurrentTime
    #     actuation.set_heating(True)
