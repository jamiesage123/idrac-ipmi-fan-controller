import pytest
from facades.FanController import FanController
from facades.IPMITool import IPMITool


@pytest.fixture
def ipmitool(mocker):
    def mockVerifyCredentails(self):
        pass

    mocker.patch(
        'facades.IPMITool.IPMITool.verifyCredentails',
        mockVerifyCredentails
    )

    def mockExecute(self, command):
        return ("stdout", "stderr")

    mocker.patch(
        'facades.IPMITool.IPMITool.execute',
        mockExecute
    )

    return IPMITool('127.0.0.1', 'root', 'calvin')


@pytest.fixture
def controller(mocker, ipmitool):
    return FanController(ipmitool)


def test_set_manual_mode(mocker, controller):
    controller.setManualMode()
    assert controller.mode == "manual"
    assert controller.getMode() == "manual"


def test_set_static_fan_mode(mocker, controller):
    controller.setStaticFanMode()
    assert controller.mode == "static"
    assert controller.getMode() == "static"


def test_set_speed(mocker, controller):
    controller.setSpeed(15)
    assert controller.speed == 15
    assert controller.getSpeed() == 15


def test_set_speed_static(mocker, controller):
    controller.setSpeed('static')
    assert controller.mode == "static"
    assert controller.getMode() == "static"
