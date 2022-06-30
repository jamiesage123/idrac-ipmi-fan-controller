import os
import time
from facades.Configuration import Configuration
from facades.IPMITool import IPMITool
from facades.TemperatureController import TemperatureController

# reqs: pythong 3.6 python3-pip3
# pip3 install -r requirements.txt
# ipmitool
# linux

def main():
    # Pipe seperate string i.e. 30,4|35,4|40,5
    rangesEnv = os.getenv('RANGES', None)

    # Parse ranges from our the envars
    if rangesEnv is not None:
        ranges = []

        for item in rangesEnv.split('|'):
            range, fanSpeed = item.split(',')
            ranges.append([int(range), int(fanSpeed)])
    else:
        # Default range
        ranges = [
            [30, 4],
            [35, 4],
            [40, 5],
            [45, 8],
            [50, 'static']
        ]

    # Set up our configuration
    config = Configuration({
        "ipmi": {
            "host": os.getenv('IDRAC_HOST'),
            "username": os.getenv('IDRAC_USERNAME'),
            "password": os.getenv('IDRAC_PASSWORD')
        },
        "monitor": {
            "range_increment": os.getenv('RANGE_INCREMENT', 5),
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