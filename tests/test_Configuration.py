import pytest
from facades.Configuration import Configuration
from facades.exceptions.InvalidConfigurationException import InvalidConfigurationException


def tests_requires_configuration():
    with pytest.raises(TypeError):
        Configuration()


def tests_configuration_none():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration(None)
    assert "Configuration must be a dictionary" in str(excinfo.value)


def tests_configuration_empty():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration("")
    assert "Configuration must be a dictionary" in str(excinfo.value)


def tests_ipmi_host_not_set():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({"ipmi": {}})
    assert "IPMI host is not configure" in str(excinfo.value)


def tests_ipmi_host_empty():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({"ipmi": {"host": ""}})
    assert "IPMI host is not configure" in str(excinfo.value)


def tests_ipmi_username_not_set():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({"ipmi": {"host": "127.0.0.1"}})
    assert "IPMI username is not configure" in str(excinfo.value)


def tests_ipmi_username_empty():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({"ipmi": {"host": "127.0.0.1", "username": ""}})
    assert "IPMI username is not configure" in str(excinfo.value)


def tests_ipmi_password_not_set():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({"ipmi": {"host": "127.0.0.1", "username": "root"}})
    assert "IPMI password is not configure" in str(excinfo.value)


def tests_ipmi_password_empty():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration(
            {"ipmi": {"host": "127.0.0.1", "username": "root", "password": ""}}
        )
    assert "IPMI password is not configure" in str(excinfo.value)


def tests_requires_monitor():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration(
            {"ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"}}
        )
    assert "Range configuration is not set up" in str(excinfo.value)


def tests_monitor_ranges_not_set():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {}
        })
    assert "Range configuration is not set up" in str(excinfo.value)


def tests_monitor_ranges_not_array():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": "123"}
        })
    assert "Range configuration must be a list" in str(excinfo.value)


def tests_monitor_ranges_overlap_one():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": [[10, 20, 'static'], [5, 30, 2]]}
        })
    assert "conflicts with" in str(excinfo.value)


def tests_monitor_ranges_overlap_two():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": [[5, 30, 2], [10, 20, 'static']]}
        })
    assert "conflicts with" in str(excinfo.value)


def tests_monitor_ranges_bad_structure():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": [[5, 2], [10]]}
        })
    assert "Range must have 3 keys" in str(excinfo.value)


def tests_monitor_ranges_not_integers():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": [["5", 30, 2], [10, "20", 'static']]}
        })
    assert "Range start and from must be integers" in str(excinfo.value)


def tests_monitor_ranges_bad_fan_speed():
    with pytest.raises(InvalidConfigurationException) as excinfo:
        Configuration({
            "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
            "monitor": {"ranges": [[5, 30, 2], [10, 20, 'bad']]}
        })
    assert "Range fan speed percentage must be an integer or 'static'" in str(
        excinfo.value
    )


def tests_configuration_get():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.get('ipmi', 'host') == "127.0.0.1"


def tests_configuration_get_bad_namespace():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.get('bad_namespace', 'bad_key') is None


def tests_configuration_get_bad_key():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.get('ipmi', 'bad_key') is None


def tests_configuration_get_only_namespace():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert type(config.get('ipmi')) is dict


def tests_configuration_filled():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.filled('ipmi', 'host') is True


def tests_configuration_not_filled():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.filled('ipmi', 'bad_key') is False


def tests_configuration_filled_namespace():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]},
    })
    assert config.filled('ipmi') is True


def tests_configuration_not_filled_namespace():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]},
    })
    assert config.filled('bad_namespace') is False


def tests_configuration():
    config = Configuration({
        "ipmi": {"host": "127.0.0.1", "username": "root", "password": "calvin"},
        "monitor": {"ranges": [[30, 40, 10], [40, 50, 'static']]}
    })
    assert config.get('ipmi', 'host') == "127.0.0.1"
    assert config.get('ipmi', 'username') == "root"
    assert config.get('ipmi', 'password') == "calvin"
    assert type(config.get('monitor', 'ranges')) is list
