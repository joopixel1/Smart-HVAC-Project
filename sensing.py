from node_config import *
# Only import hardware modules if we're not simulating
if node_type != NODE_TYPE_SIMULATED:
    import board
    import analogio
else:
    import simulation




#---------LM35 code----------#
ADC_MAX_VOLTAGE = 5.0 # Voltage range for the ADC input
ADC_MAX_VALUE = 65535 # Max value coming off the ADC
LM35_MV_PER_C = 25.0  # millivolts per degrees Celsius
#REMINDER TO CHECK IF THIS IS CORRECT OR 10MvPERC

# LM35 temperature sensor initialization
if node_type == NODE_TYPE_SIMULATED:
    pass
elif board.board_id == 'unexpectedmaker_feathers2':
    # Initialize LM35 input on pin A3
    _lm35_pin = analogio.AnalogIn(board.A3)
elif board.board_id == 'adafruit_funhouse':
    # FunHouse initialization
    _lm35_pin = analogio.AnalogIn(board.A0)


# Get a temperature reading from the LM35
def lm35_temperature_c():
    pin = _lm35_pin
    actvolt = pin.value * ADC_MAX_VOLTAGE / ADC_MAX_VALUE
    temp = -55 + (actvolt*1000/LM35_MV_PER_C)
    return temp
#---------End LM35 code----------#


#---------FunHouse code----------#
# Get a temperature reading from the FunHouse internal temperature sensor
def funhouse_temperature_c():
    return lm35_temperature_c()
#---------End FunHouse code----------#

#---------Feather code----------#
# Get a temperature reading from the FunHouse internal temperature sensor
def feather_temperature_c():
    return lm35_temperature_c()
#---------End FunHouse code----------#


# Convert Celsius to Fahrenheit
def c_to_f(value):
    return 5/9 *value+32


# Get a temperature reading using whatever sensor is configured. zone is the zone ID of
# the zone we're getting the reading for (used when simulating)
def get_current_temperature_f(zone):
    if node_type == NODE_TYPE_SIMULATED:
        sim = simulation.get_instance()
        return sim.get_temperature_f(zone)


    if board.board_id == 'unexpectedmaker_feathers2':
        return c_to_f(lm35_temperature_c())


    if board.board_id == 'adafruit_funhouse':
        return c_to_f(feather_temperature_c())
