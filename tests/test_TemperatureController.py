import pytest
from facades.IPMITool import IPMITool
from facades.Configuration import Configuration
from facades.TemperatureController import TemperatureController
from facades.exceptions.CustomException import CustomException


@pytest.fixture
def ipmitool(mocker):
    def mockVerifyCredentails(self):
        pass

    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    return IPMITool('127.0.0.1', 'root', 'calvin')


def test_get_current_temperatures(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ok  |  3.1 | 50 degrees C
               Temp             | 0Fh | ok  |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })

    assert type(TemperatureController(
        config, ipmitool).getCurrentTemperatures()
    ) is list


def test_get_current_temperatures_skips_bad_sensors(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ns  |  3.1 | 50 degrees C
               Temp             | 0Fh |     |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })

    temperatures = list(map(lambda x: x['value'], TemperatureController(
        config, ipmitool
    ).getCurrentTemperatures()))

    assert 31 in temperatures
    assert 40 in temperatures
    assert 50 not in temperatures
    assert 44 not in temperatures


def test_get_current_temperatures_static_fallback_on_error(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            None,
            "I am an error"
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })

    mock = mocker.patch('facades.FanController.FanController.setStaticFanMode')

    with pytest.raises(CustomException):
        TemperatureController(config, ipmitool).getCurrentTemperatures()

    mock.assert_called()


def test_monitor_sets_correct_fan_speed(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ok  |  3.1 | 49 degrees C
               Temp             | 0Fh | ok  |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 30]]}
    })

    mock = mocker.patch('facades.FanController.FanController.setSpeed')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called_with(30)


def test_monitor_sets_correct_fan_speed_complex(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 45 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 46 degrees C
               Temp             | 0Eh | ok  |  3.1 | 47 degrees C
               Temp             | 0Fh | ok  |  3.2 | 48 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [
            [20, 25, 5], [25, 30, 10], [25, 30, 15], [30, 35, 20],
            [35, 40, 25], [40, 45, 30], [45, 50, 35], [55, 60, 40]
        ]}
    })

    mock = mocker.patch('facades.FanController.FanController.setSpeed')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called_with(35)


def test_monitor_fallback_highest_range(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ok  |  3.1 | 49 degrees C
               Temp             | 0Fh | ok  |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[10, 20, 10], [20, 30, 45]]}
    })

    mock = mocker.patch('facades.FanController.FanController.setSpeed')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called_with(45)


def test_monitor_fallback_lowest_range(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 23 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 23 degrees C
               Temp             | 0Eh | ok  |  3.1 | 23 degrees C
               Temp             | 0Fh | ok  |  3.2 | 23 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [50, 60, 45]]}
    })

    mock = mocker.patch('facades.FanController.FanController.setSpeed')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called_with(10)


def test_monitor_static_range(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ok  |  3.1 | 49 degrees C
               Temp             | 0Fh | ok  |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[10, 20, 10], [30, 50, 'static'], [50, 60, 50], [60, 90, 100]]}
    })

    mock = mocker.patch('facades.FanController.FanController.setSpeed')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called_with('static')


def test_monitor_fallback_to_static_without_range(mocker, ipmitool):
    def mockExecute(self, command):
        return (
            """Inlet Temp       | 04h | ok  |  7.1 | 31 degrees C
               Exhaust Temp     | 01h | ok  |  7.1 | 40 degrees C
               Temp             | 0Eh | ok  |  3.1 | 49 degrees C
               Temp             | 0Fh | ok  |  3.2 | 44 degrees C""",
            None
        )

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[10, 20, 10], [30, 50, 'static'], [50, 60, 50], [60, 90, 100]]}
    })

    def mockClosestRange(self, command):
        return None

    mocker.patch(
        'facades.TemperatureController.Ranges.closestRange',
        mockClosestRange
    )

    mock = mocker.patch('facades.FanController.FanController.setStaticFanMode')

    TemperatureController(config, ipmitool).monitor()

    mock.assert_called()
