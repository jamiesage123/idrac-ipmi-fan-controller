from facades.TemperatureController import Ranges
from facades.exceptions.InvalidConfigurationException import InvalidConfigurationException


class Configuration:
    """
    Represents a facade for setting and retreiving configuration options
    """

    def __init__(self, config):
        self.config = config
        self.validate()

    """
    Get a configuration setting
    Parameters
    ----------
    namespace or key : str
        The configuration namespace (or the key if no namespace)
    key : str
        The configuration key
    """

    def get(self, *args):
        if len(args) == 2:
            namespace, key = args

            if namespace not in self.config or key not in self.config[namespace]:
                return None

            return self.config[namespace][key]
        else:
            if args[0] not in self.config:
                return None

            return self.config[args[0]]

    """
    Determine if a configuration setting is filled (i.e. not empty)
    Parameters
    ----------
    namespace or key : str
        The configuration namespace (or the key if no namespace)
    key : str
        The configuration key
    """

    def filled(self, *args):
        value = self.get(*args)
        return value is not None and value != ""

    """
    Validate all configurations
    """

    def validate(self):
        if type(self.config) is not dict:
            raise InvalidConfigurationException(
                'Configuration must be a dictionary'
            )

        self.validateIPMITool()
        self.validateRanges()

    """
    Validate the IPMI Tool configuration
    """

    def validateIPMITool(self):
        if not self.filled('ipmi', 'host'):
            raise InvalidConfigurationException('IPMI host is not configured')

        if not self.filled('ipmi', 'username'):
            raise InvalidConfigurationException(
                'IPMI username is not configured'
            )

        if not self.filled('ipmi', 'password'):
            raise InvalidConfigurationException(
                'IPMI password is not configured'
            )

    """
    Validate the range configuration
    """

    def validateRanges(self):
        # Ensure that we have ranges set up
        if not self.filled('monitor', 'ranges'):
            raise InvalidConfigurationException(
                'Range configuration is not set up'
            )

        # Fetch the ranges
        ranges = Ranges(self.get('monitor', 'ranges'))

        # Ensure there is no overlaps in the configured ranges
        for x in ranges.all():
            for y in ranges.all():
                if ranges.overlaps(x, y):
                    raise InvalidConfigurationException(
                        f'Temperature range {x[0]} to {x[1]} conflicts with {y[0]} to {y[1]}'
                    )
