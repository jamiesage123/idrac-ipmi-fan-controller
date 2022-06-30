class Configuration:
    """
    Represents a facade for setting and retreiving configuration options
    """

    def __init__(self, config):
        self.config = config

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
            return self.config[namespace][key]
        else:
            key = args
            return self.config[key]
