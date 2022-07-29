from datetime import datetime
from tabulate import tabulate
from facades.FanController import FanController
from facades.parsers.TabbedTable import TabbedTable
from facades.exceptions.InvalidConfigurationException import InvalidConfigurationException

class TemperatureController:
    """
    Represents a facade for controlling iDRAC temperature
    """

    def __init__(self, config, ipmitool):
        self.ipmitool = ipmitool
        self.fanController = FanController(ipmitool)
        self.ranges = config.get('monitor', 'ranges')
        
    """
    Get the current temperature fom the sensors
    """
    def getCurrentTemperatures(self):
        output, err = self.ipmitool.execute('sdr type temperature')

        # If there were any errors, fallback to static fan mode
        if err != "" or err is None:
            self.fanController.setStaticFanMode()
            print(err)
                        
        # Parse the output
        values = TabbedTable(output).all()

        temperatures = []

        for data in values:
            name, value1, status, value2, temperature = data

            # Skip irrevalant sensors
            if status == 'ns' or status == '':
                continue

            temperatures.append({"name": name.replace(" Temp", ""), "value": int(temperature.split(' ')[0])})
                    
        return temperatures

    """
    Run the temperature monitoring logic
    """
    def monitor(self):
        # TODO: We dont need to monitor if the machine is in the "off" state

        # Set up our ranges
        ranges = Ranges(self.ranges)

        # Fetch the lowest range
        lowestRange = ranges.lowestRange()

        # Fetch the highest range
        highestRange = ranges.highestRange()

        # Fetch the current temperatures
        temperatures = self.getCurrentTemperatures()

        # Find the hottest sensor
        temperature = max(map(lambda x: x['value'], temperatures))

        # The selected range we're going to usw
        selectedRange = None

        # Text notes to display at the end
        notes = ""

        # Loop through our ranges and find the range that we should be in
        for rangeConfig in ranges.all():
            startOfRange, endOfRange, fanSpeed = rangeConfig

            # If our temperature falls into this range, select it
            if temperature >= startOfRange and temperature <= endOfRange:
                selectedRange = rangeConfig
        
        # If our temperature doesn't fall into any pre-defined ranges, attempt to find the closest range
        if selectedRange is None:
            fallBackRange = None

            # Find the closest range
            if (temperature - lowestRange) > (temperature - highestRange):
                fallBackRange = highestRange
            else:
                fallBackRange = lowestRange

            # Find the fallback range
            for rangeConfig in ranges.all():
                if rangeConfig[0] == fallBackRange:
                    selectedRange = rangeConfig
                    notes = f'Temperature outside of configured ranges, falling back to closest configuration ({rangeConfig[0]} - {rangeConfig[1]})'
        
        # If we still dont have a range, fall back to static fan mode
        if selectedRange is None:
            notes = "No range configured for temperature, falling back to static fan mode"
            self.fanController.setStaticFanMode()
        else:
            # Get the selected range details
            startOfRange, endOfRange, fanSpeed = selectedRange

            # Set the speed
            self.fanController.setSpeed(fanSpeed)

            # Update the notes
            if notes == "":
                notes = f'Using configured range {startOfRange} to {endOfRange}'

        # Print the results to the console
        self.printResults(temperatures, notes)
        
    def printResults(self, temperatures, notes):
        # Get the mode that we just set to
        mode = self.fanController.getMode()

        # Get the speed we just set to
        speed = self.fanController.getSpeed()

        output = [[
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            f'{mode} ({speed}%)' if mode == 'manual' else mode,
            ", ".join(map(lambda x: f'{str(x["name"])}: {str(x["value"])}', temperatures)),
            notes
        ]]

        print(tabulate(output, headers=['Timestamp', 'Fan mode', 'Temperatures', 'Notes']))
        print('\n')

class Ranges:
    """
    Represents a facade for dealing with ranges
    """

    def __init__(self, ranges):
        # Validate the ranges
        if type(ranges) is not list:
            raise InvalidConfigurationException('Range configuration must be a list')

        for x in ranges:
            if len(x) != 3:
                raise InvalidConfigurationException('Range must have 3 keys (i.e. 30, 20, \'static\')')
            if type(x[0]) is not int or type(x[1]) is not int:
                raise InvalidConfigurationException('Range start and from must be integers')
            if type(x[2]) is not int and x[2] != "static":
                raise InvalidConfigurationException('Range fan speed percentage must be an integer or \'static\'')
            
        self.ranges = self.sort(ranges)

    """
    Sort an array of ranges to be in order of smallest to largest
    """
    def sort(self, ranges):
        ranges.sort(key=lambda x: x[0])
        return ranges

    """
    Determine if two ranges overlap
    """
    def overlaps(self, x, y):
        return x[0] != y[0] and ((x[1] - 1) >= (y[0]) and (y[1] - 1) >= (x[0]))

    """
    Get the highest range
    """
    def highestRange(self):
        return max(map(lambda x: x[0], self.ranges))

    """
    Get the lowest range
    """
    def lowestRange(self):
        return min(map(lambda x: x[0], self.ranges))

    """
    Get all ranges
    """
    def all(self):
        return self.ranges