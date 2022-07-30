import pytest
from facades.IPMITool import IPMITool
from facades.exceptions.IPMIConnectionException import IPMIConnectionException
from facades.exceptions.IPMIToolShellException import IPMIToolShellException
from facades.exceptions.InvalidConfigurationException import InvalidConfigurationException

def tests_requires_configuration():
    with pytest.raises(TypeError):
        IPMITool()

def tests_requires_host():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        IPMITool('', 'username', 'password')
    assert "Host, username and password must be provided" in str(excinfo.value)

def tests_requires_username():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        IPMITool('127.0.0.1', '', 'password')
    assert "Host, username and password must be provided" in str(excinfo.value)

def tests_requires_password():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        IPMITool('127.0.0.1', 'root', '')
    assert "Host, username and password must be provided" in str(excinfo.value)

def tests_raises_error_failed_connection(mocker):
    def mockVerifyCredentails(self):
        raise IPMIConnectionException()
        
    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    with pytest.raises(IPMIConnectionException):
        IPMITool('127.0.0.1', 'root', 'calvin')

def tests_connection_string(mocker):
    def mockVerifyCredentails(self):
        pass
        
    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    assert IPMITool('127.0.0.1', 'root', 'calvin').connectionString() == '-I lanplus -H 127.0.0.1 -U root -P calvin'

def test_verify_credentials(mocker, capfd):
    def mockExecute(self, command):
        return (
            """Product Name    :    Dell Server
               Item One        :    Value
               Item Two        :    Value2""",
            None
        )
        
    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    IPMITool('127.0.0.1', 'root', 'calvin').verifyCredentails()

    assert "Successfully connected to Dell Server" in str(capfd.readouterr().out)

def test_verify_credentials_error(mocker, capfd):
    def mockExecute(self, command):
        return (
            None,
            "I am an error"
        )
        
    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    with pytest.raises(IPMIConnectionException):
        IPMITool('127.0.0.1', 'root', 'calvin').verifyCredentails()

    assert "Unable to connect to IPMI Tool. Please check your host, username and password." in str(capfd.readouterr().out)

def test_execute(mocker, fp):
    def mockVerifyCredentails(self):
        pass
        
    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    out = """Product Name    :    Dell Server
               Item One      :    Value
               Item Two      :    Value2"""

    fp.register(
        "ipmitool -I lanplus -H 127.0.0.1 -U root -P calvin test command",
        stdout=out, stderr=""
    )

    stdout, stderr = IPMITool('127.0.0.1', 'root', 'calvin').execute('test command')

    assert stdout == out
    assert stderr is ""

def test_execute_shell_error(mocker, fp):
    def mockVerifyCredentails(self):
        pass
        
    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    fp.register(
        "ipmitool -I lanplus -H 127.0.0.1 -U root -P calvin test command",
        stderr="/bin/sh: Shell error"
    )

    with pytest.raises(IPMIToolShellException) as excinfo:
        IPMITool('127.0.0.1', 'root', 'calvin').execute('test command')

    assert "/bin/sh: Shell error" in str(excinfo.value)

def test_execute_connection_error(mocker, fp):
    def mockVerifyCredentails(self):
        pass
        
    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    fp.register(
        "ipmitool -I lanplus -H 127.0.0.1 -U root -P calvin test command",
        stderr="Error: Unable to establish IPMI v2 / RMCP+ session"
    )

    with pytest.raises(IPMIConnectionException) as excinfo:
        IPMITool('127.0.0.1', 'root', 'calvin').execute('test command')

    assert "Error: Unable to establish IPMI v2 / RMCP+ session" in str(excinfo.value)
