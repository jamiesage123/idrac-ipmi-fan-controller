import os
import time
from facades.Configuration import Configuration
from facades.IPMITool import IPMITool
from facades.TemperatureController import TemperatureController


def main():
    # Set up our configuration
    config = Configuration({
        "ipmi": {
            "host": os.getenv('IDRAC_HOST'),
            "username": os.getenv('IDRAC_USERNAME'),
            "password": os.getenv('IDRAC_PASSWORD')
        },
        "monitor": {
            "ranges": parseRanges(os.getenv('TEMP_RANGES', None))
        }
    })

    # Set up IPMI Tool
    ipmitool = IPMITool(
        config.get('ipmi', 'host'),
        config.get('ipmi', 'username'),
        config.get('ipmi', 'password')
    )

    # Set up the Temperature Controller
    tempController = TemperatureController(config, ipmitool)

    # TODO: better
    intervals = 30.0
    starttime = time.time()

    while True:
        # Start the temperature monitor
        tempController.monitor()

        time.sleep(intervals - ((time.time() - starttime) % intervals))


def parseRanges(rangesEnv):
    ranges = None

    # Parse ranges from our the envars
    if rangesEnv is not None:
        ranges = []

        for item in rangesEnv.split('|'):
            # Remove any whitespaces from the range config
            item = map(lambda x: x.strip(), item.split(','))

            # Extract the start, end and fan speed percentage
            startOfRange, endOfRange, fanSpeed = item

            ranges.append([
                int(startOfRange), int(endOfRange),
                fanSpeed if fanSpeed == 'static' else int(fanSpeed)
            ])

    return ranges


if __name__ == "__main__":
    main()
