from node_config import *
# Don't import hardware libraries if simulating
if node_type != NODE_TYPE_SIMULATED:
    import board
    import digitalio
    import pwmio
    from adafruit_motor import servo
else:
    import simulation
    # import time




#------------Damper control-----------#
# Parallax Standard Servo (https://www.parallax.com/product/parallax-standard-servo/)
SERVO_ACTUATION_RANGE = 180  #degrees
SERVO_MIN_PULSE = 750 #us, for PWM control
SERVO_MAX_PULSE = 2250 #us, for PWM control

# Damper initialization
if node_type == NODE_TYPE_SIMULATED:
    pass
else: 
    # Damper initialization - use pins A0, A1, and A2 for zones 1, 2, and 3 respectively
    pwmZone1 = pwmio.PWMOut(board.A0, duty_cycle=0, frequency=50)
    pwmZone2 = pwmio.PWMOut(board.A1, duty_cycle=0, frequency=50)
    pwmZone3 = pwmio.PWMOut(board.A2, duty_cycle=0, frequency=50)
    servoZone = []
    servoZone.append(servo.Servo(pwmZone1, SERVO_ACTUATION_RANGE, SERVO_MIN_PULSE, SERVO_MAX_PULSE))
    servoZone.append(servo.Servo(pwmZone2, SERVO_ACTUATION_RANGE, SERVO_MIN_PULSE, SERVO_MAX_PULSE))
    servoZone.append(servo.Servo(pwmZone3, SERVO_ACTUATION_RANGE, SERVO_MIN_PULSE, SERVO_MAX_PULSE))

# Set the damper for the given zone to the given percent (0 means open, 100 means fully closed)
def set_damper(zone, percent):

    print("actually editing it.")

    if percent >=100:
        percent =100
    elif percent<=0:
        percent =0
    
    if node_type != NODE_TYPE_SIMULATED:
        # Write your code so that it will NEVER set the servos to any angle outside of the range [45, 135]
        servoZone[zone].angle = 45 + (percent* 90/100)
    else:
        sim = simulation.get_instance()
        sim.set_damper(zone, percent)

# Get a damper percent reading for a zone
def get_damper_position(zone):
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.get_damper_pos(zone)
    else: 
        return (servoZone[zone].angle - 45) *100 / 90
    
#------------End damper control-----------#




#------------Heat/cool control-----------#
# pin configuration
if node_type == NODE_TYPE_SIMULATED:
    pass
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize digital outputs for heating, cooling, and the circulation fan
    # Use pins D13 for heat, D9 and D6 for cooling, and D12 for the fan
    pinHeat = digitalio.DigitalInOut(board.D13)
    pinCool = digitalio.DigitalInOut(board.D9)
    pinFan = digitalio.DigitalInOut(board.D12)
    pinHeat.direction = digitalio.Direction.OUTPUT
    pinCool.direction = digitalio.Direction.OUTPUT
    pinFan.direction = digitalio.Direction.OUTPUT
else:
    pass


# Control the heater (turn on by passing in True, off by passing in False)
# and ensures heating and cooling cannot work together
def set_heating(value: bool):
    if node_type != NODE_TYPE_SIMULATED:
        pinHeat.value = value
        if pinHeat.value == True: 
            pinCool.value = False
            set_circulating(True)
        else:
            if pinCool.value == False: set_circulating(False)
    else:
        sim = simulation.get_instance()
        sim.heat = value
        if sim.heat == True: 
            sim.cool = False
            set_circulating(True)
        else:
            if sim.cool == False: set_circulating(False)


# Control the cooler (turn on by passing in True, off by passing in False)
# and ensures heating and cooling cannot work together
#also turn on or off the fan if the cooler or heater is on.
def set_cooling(value: bool):
    if node_type != NODE_TYPE_SIMULATED:
        pinCool.value = value
        if pinCool.value == True: 
            pinHeat.value = False
            set_circulating(True)
        else:
            if pinHeat.value == False: set_circulating(False)
    else:
        sim = simulation.get_instance()
        sim.cool = value
        if sim.cool == True: 
            sim.heat = False
            set_circulating(True)
        else:
            if sim.heat == False: set_circulating(False)

# Control the circulation fan (turn on by passing in True, off by passing in False)
def set_circulating(value: bool):
    if node_type != NODE_TYPE_SIMULATED:
        pinFan.value = value
    else:
        sim = simulation.get_instance()
        sim.fan = value

# Get whether is heating is on or off
def get_heater() -> int:
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.heat
    else: 
        return pinHeat.value
    
# Get whether is cooler is on or off
def get_cooler() -> int:
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.cool
    else: 
        return pinCool.value
    
def get_fan() -> int:
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.fan
    else: 
        return pinFan.value

#------------End heat/cool control-----------#







