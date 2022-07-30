<div id="top"></div>

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/jamiesage123/idrac-ipmi-fan-controller?include_prereleases&style=for-the-badge)
![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/jamiesage123/idrac-ipmi-fan-controller/Docker%20Image%20CI?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/jamiesage123/idrac-ipmi-fan-controller?style=for-the-badge)


<br />
<div align="center">
    <h3 align="center">iDRAC IPMI Fan Controller</h3>

  <p align="center">
    Automatically control Dell PowerEdge fans using IPMI
  </p>
</div>

<ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-local">Installation (local)</a></li>
        <li><a href="#environment-variables">Environment variables</a></li>
        <ul>
            <li><a href="#temperature-ranges">Temperature ranges</a></li>
        </ul>
      </ul>
    </li>
    <li><a href="#usage-local">Usage (local)</a></li>
    <li><a href="#usage-docker">Usage (Docker)</a></li>
    <li><a href="#tests">Tests</a></li>
    <li><a href="#code-style-standards">Code style standards</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>

## About The Project
This project allows you to automatically control your Dell PowerEdge fan speeds using IPMI tools determined by a customisable temperature range.


<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* [Python](https://www.python.org/)
* [IPMI Tools](https://github.com/ipmitool/ipmitool)
* [tabulate](https://pypi.org/project/tabulate/)
* [pytest](https://docs.pytest.org/)
* [pytest-mock](https://pypi.org/project/pytest-mock/)
* [coverage](https://pypi.org/project/coverage//)
* [pytest-subprocess](https://pypi.org/project/pytest-subprocess/)
* [flake8](https://flake8.pycqa.org/en/latest/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

* Python 3.8
* Python pip3
* IPMI Tools ([https://github.com/ipmitool/ipmitool](https://github.com/ipmitool/ipmitool))

### Installation (local)

After installing the projects prerequisites, you will need to install the projects python dependencies using pip3

1. Install Python dependencies using pip3
   ```sh
   pip3 install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


### Environment variables

This project depends on several environment variables being available to the script, these are described below

| Variable       | Default | Description                                                           |
|----------------|---------|-----------------------------------------------------------------------|
| `IDRAC_HOST`     | `null`  | IP address of your iDRAC host                                         |
| `IDRAC_USERNAME` | `null`  | Username of your iDRAC host                                           |
| `IDRAC_PASSWORD` | `null`  | Password of your iDRAC host                                           |
| `TEMP_RANGES`    | `null`  | Pipe-separated list of temperature ranges, see below for more details |

<p align="right">(<a href="#top">back to top</a>)</p>


#### Temperature ranges

The temperature ranges environment variable allows you to define a range of temperatures and your desired fan speed (as a percentage). This is set using a pipe-separated string provided as an environment variable (`TEMP_RANGES`).

Format:  
`[start of range], [end of range], [fan speed percentage]|[start of range], [end of range], [fan speed percentage]`

For example:  
`30, 40, 5|40, 45, 8|45, 50, 10|50, 55, 20|55, 100, static`

This will be parsed as:

| Temperature | Fan speed |
|-------------|-----------|
| 30c to 40c  | 5%        |
| 40c to 45c  | 8%        |
| 45c to 50c  | 10%       |
| 50c to 55c  | 20%       |
| 55c to 100c | static    |

`static` fan speed mode will turn off manual fan control and allow iDRAC to determine what speed the fans should be for the current temperature (default behaviour).

If there isn't a temperature range configured, this tool will use the closest temperature range based on the highest temperature sensor.

<p align="right">(<a href="#top">back to top</a>)</p>


## Usage (local)

To run the project locally, execute the `controller.py` file

```sh
python3 controller.py
```

## Usage (Docker)

You can run this project using docker by pulling and running the pre-build image using the following command

```sh
docker run -d \
  --name iDRAC_IPMI_fan_controller \
  --restart=unless-stopped \
  -e IDRAC_HOST=<iDRAC host> \
  -e IDRAC_USERNAME=<iDRAC username> \
  -e IDRAC_PASSWORD=<iDRAC password> \
  -e TEMP_RANGES=<pipe seperated list of temp ranges> \
  jamiesage123/idrac-ipmi-fan-controller:latest
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- TESTS -->
## Tests

Tests are located in the `tests` directory. Before you can run the tests, you must install the test dependencies using pip3

1. Install test dependencies using pip3
   ```sh
   pip3 install -r tests/requirements.txt
   ```

You can now run the project tests

2. Run pytest
   ```sh
   pytest tests
   ```

This project aims to have >= 95% test coverage. You can check the projects test coverage by running:

1. Test coverage
   ```sh
   coverage run -m pytest tests
   ```

<!-- LINT -->
## Code style standards

This project uses Flake8 to enforce code style standards to style conventions in [PEP 8](https://peps.python.org/pep-0008/).

You can run Flake8 by installing the <a href="#tests">test dependencies</a> and then running:

1. Run lint
   ```sh
   flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
   ```

<!-- CONTRIBUTING -->
## Contributing

Contributions make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion to improve this, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this project at your own risk and responsibility. Overriding default behaviour may cause irreversible damage to hardware. Always monitor and ensure your hardware is running at safe temperatures.

This project is released under the MIT License.

<p align="right">(<a href="#top">back to top</a>)</p>
