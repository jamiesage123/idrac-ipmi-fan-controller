import subprocess
from facades.parsers.TabbedList import TabbedList
from facades.exceptions.IPMIToolShellException import IPMIToolShellException
from facades.exceptions.IPMIConnectionException import IPMIConnectionException
from facades.exceptions.InvalidConfigurationException import InvalidConfigurationException


class IPMITool:
    """
    Represents a facade for authenticating with and executing ipmitool commands
    """

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.verifyCredentails()

    """
    Check the credentials provided can authenticate with ipmitool
    """

    def verifyCredentails(self):
        # Verify that we have the required credentials
        if self.host == "" or self.username == "" or self.password == "":
            raise InvalidConfigurationException(
                "Host, username and password must be provided"
            )

        try:
            # Attempt to retrieve basic info from IPMI
            output, err = self.execute('fru')

            if err is not None and err != "":
                raise IPMIConnectionException(err)

            # Parse the products name
            productName = TabbedList(output).get('Product Name')

            print(
                f'Successfully connected to {productName if productName is not None else "Unknown"}')
        except IPMIConnectionException as err:
            print(
                "Unable to connect to IPMI Tool. Please check your host, username and password.")
            raise err

    """
    Generate the connection string to be used when executing an IPMI Tool command
    """

    def connectionString(self):
        return f'-I lanplus -H {self.host} -U {self.username} -P {self.password}'

    """
    Execute an IPMI Tool command
    """

    def execute(self, command):
        arg = f'ipmitool {self.connectionString()} {command}'

        # Execute the command
        process = subprocess.Popen(
            arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Fetch the response from the command
        stdout, stderr = process.communicate()

        # Decode the output message
        stdout = stdout.decode("utf-8")

        # Decode any error messages
        stderr = stderr.decode("utf-8")

        # Handle shell related errors
        if "/bin/sh:" in stderr:
            raise IPMIToolShellException(stderr)

        # Handle connection related errors
        if "Error: Unable to establish IPMI v2 / RMCP+ session" in stderr:
            raise IPMIConnectionException(stderr)

        return (stdout, stderr)
