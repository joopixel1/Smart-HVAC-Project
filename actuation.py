from node_config import *
# Don't import hardware libraries if simulating
import board
import digitalio
import time
import simulation
import pwmio
from adafruit_motor import servo

pinHeat = digitalio.DigitalInOut(board.D13)
pinCool = digitalio.DigitalInOut(board.D9)
pinHeat.direction = digitalio.Direction.OUTPUT
pinCool.direction = digitalio.Direction.OUTPUT
#------------Damper control-----------#
# Parallax Standard Servo (https://www.parallax.com/product/parallax-standard-servo/)
SERVO_ACTUATION_RANGE = 180  #degrees
SERVO_MIN_PULSE = 750 #us, for PWM control
SERVO_MAX_PULSE = 2250 #us, for PWM control

if node_type != NODE_TYPE_SIMULATED:
    # Damper initialization - use pins A0, A1, and A2 for zones 1, 2, and 3 respectively
    # TODO: damper initialization
    pwmZone1 = pwmio.PWMOut(board.A0, duty_cycle=0, frequency=50)
    pwmZone2 = pwmio.PWMOut(board.A1, duty_cycle=0, frequency=50)
    pwmZone3 = pwmio.PWMOut(board.A2, duty_cycle=0, frequency=50)
    servoZone = []
    servoZone.append(servo.Servo(pwmZone1))
    servoZone.append(servo.Servo(pwmZone2))
    servoZone.append(servo.Servo(pwmZone3))

# Set the damper for the given zone to the given percent (0 means closed, 100 means fully open)
def set_damper(zone, percent):
    # TODO: damper control
    if percent >=100:
        percent =100
    elif percent<=0:
        percent =0
    servoZone[zone].angle = 45 + (90*percent/100)
    sim = simulation.get_instance()
    sim.set_damper(zone, percent)
    
#------------End damper control-----------#

#------------Heat/cool control-----------#
# TODO: pin configuration
if node_type == NODE_TYPE_SIMULATED:
    pass
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize digital outputs for heating, cooling, and the circulation fan
    # Use pins D13 for heat, D9 and D6 for cooling, and D12 for the fan

    pass
else:
    pass

# Control the heater (turn on by passing in True, off by passing in False)
def set_heating(value):
    # TODO: heater control
    sim = simulation.get_instance()
    pinHeat.value = value
    sim.heat = value
    sim.cool = not value

# Control the cooler (turn on by passing in True, off by passing in False)
def set_cooling(value):
    # TODO: cooler control
    sim = simulation.get_instance()
    pinCool.value = value
    sim.cool = value
    sim.heat =  not value

# Control the circulation fan (turn on by passing in True, off by passing in False)
def set_circulating(value):
    # TODO: circulation fan control
    pass
#------------End heat/cool control-----------#