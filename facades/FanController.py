class FanController:
    """
    Represents a facade for controlling iDRAC fans using ipmitool
    """

    def __init__(self, ipmitool):
        self.ipmitool = ipmitool
        self.mode = None
        self.speed = None

    """
    Set the fan mode to manual
    """

    def setManualMode(self):
        if self.mode == 'manual':
            return

        self.mode = 'manual'
        return self.ipmitool.execute('raw 0x30 0x30 0x01 0x00')

    """
    Set the fan mode to "static"
    """

    def setStaticFanMode(self):
        if self.mode == 'static':
            return

        self.mode = 'static'
        return self.ipmitool.execute('raw 0x30 0x30 0x01 0x01')

    """
    Set the fan speed (percentage)
    """

    def setSpeed(self, percentage):
        if (percentage == 'static'):
            return self.setStaticFanMode()

        if self.speed == percentage:
            return

        self.setManualMode()
        self.speed = percentage
        return self.ipmitool.execute(f'raw 0x30 0x30 0x02 0xff {hex(percentage)}')

    """
    Get the current fan speed (percentage)
    """

    def getSpeed(self):
        return self.speed

    """
    Get the current fan mode
    """

    def getMode(self):
        return self.mode
