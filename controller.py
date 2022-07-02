import os
import time
from facades.Configuration import Configuration
from facades.IPMITool import IPMITool
from facades.TemperatureController import TemperatureController

# reqs: pythong 3.6 python3-pip3
# pip3 install -r requirements.txt
# ipmitool
# linux

# envars
# IDRAC_HOST
# IDRAC_USERNAME
# IDRAC_PASSWORD
# TEMP_RANGES

def main():
    # Pipe seperate string i.e. 30,4|35,4|40,5
    rangesEnv = os.getenv('TEMP_RANGES', None)

    # Parse ranges from our the envars
    if rangesEnv is not None:
        ranges = []

        for item in rangesEnv.split('|'):
            range, fanSpeed = item.split(',')
            ranges.append([int(range), fanSpeed if fanSpeed == 'static' else int(fanSpeed)])
    else:
        # Default range
        # [startOfRange, endOfRange, fanSpeed (percentage or 'static')]
        ranges = [
            [30, 40, 4],
            [40, 45, 5],
            [45, 50, 8],
            [50, 55, 10],
            [55, 100, 'static']
        ]

    # Set up our configuration
    config = Configuration({
        "ipmi": {
            "host": os.getenv('IDRAC_HOST'),
            "username": os.getenv('IDRAC_USERNAME'),
            "password": os.getenv('IDRAC_PASSWORD')
        },
        "monitor": {
            "ranges": ranges
        }
    })

    # Set up IPMI Tool
    ipmitool = IPMITool(config)

    # Set up the Temperature Controller
    tempController = TemperatureController(config, ipmitool)


    # TODO: better
    intervals = 30.0
    starttime = time.time()

    while True:
        # Start the temperature monitor
        tempController.monitor()

        time.sleep(intervals - ((time.time() - starttime) % intervals))

if __name__ == "__main__":
    main()