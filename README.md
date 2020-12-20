![GitHub release (latest by date)](https://img.shields.io/github/v/release/GuyLewin/home-assistant-crunch-o-meter)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

# About

This integration uses [Crunch Gym](https://crunch.com)'s Crunch-O-Meter API in order to monitor the amount of people currently in a Crunch club, and the maximal amount the club can have. It only works in Club locations with Crunch-O-Meter support.

# Installation

## 1. Easy Mode

Install via HACS.

## 2. Manual

Install it as you would do with any HomeAssistant custom component:

1. Download the `custom_components` folder from this repository.
1. Copy the `crunch_o_meter` directory within the `custom_components` directory of your HomeAssistant installation. The `custom_components` directory resides within the HomeAssistant configuration directory.
**Note**: if the custom_components directory does not exist, it needs to be created.
After a correct installation, the configuration directory should look like the following.
    ```
    └── ...
    └── configuration.yaml
    └── custom_components
        └── crunch_o_meter
            └── __init__.py
            └── club.py
            └── config_flow.py
            └── const.py
            └── manifest.json
            └── sensor.py
    ```

# Club Configuration

Once the component has been installed, you need to configure it with the relevant clubs. To do that, follow the following steps:
1. From the HomeAssistant web panel, navigate to 'Configuration' (on the sidebar) then 'Integrations'. Click `+` button in botton right corner,
search '**Crunch-O-Meter**' and click 'Configure'.
1. Select your Crunch club from the drop-down list. Every club is written in the `{STATE} - {CITY} - {CLUB NAME}` format. Hit submit when selected.
1. You're done!

If you want to follow more than 1 club, just follow the same steps to add additional clubs. Be sure to select different clubs every time.

## Usage

There are 2 sensors created for every club configured:
* `crunch_<club_name>_current_occupancy`
* `crunch_<club_name>_max_occupancy`

You can use the built-in [Gauge Lovelace card](https://www.home-assistant.io/lovelace/gauge/) to show the current amount of people in a club:
![Crunch-O-Meter Gauge Lovelace Card](img/gauge.png?raw=true "Crunch-O-Meter Gauge Lovelace Card")
