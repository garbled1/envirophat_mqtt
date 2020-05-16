# Envirophat MQTT
Poll a Pimoroni envirophat and publish to MQTT

## Install

`pip install envirophat_mqtt`

`python3 ./setup.py sdist install`

## Configure

    usage: envirophat_mqtt [-h] [--mqtt_host MQTT_HOST] [--mqtt_topic MQTT_TOPIC]
                       [--mqtt_clientid MQTT_CLIENTID] [--mqtt_port MQTT_PORT]
                       [--poll_time POLL_TIME] [--overscan OVERSCAN]

    optional arguments:
      -h, --help            show this help message and exit
      --mqtt_host MQTT_HOST
                            MQTT host
      --mqtt_topic MQTT_TOPIC
                            MQTT topic
      --mqtt_clientid MQTT_CLIENTID
                            MQTT client ID
      --mqtt_port MQTT_PORT
                            MQTT port
      --poll_time POLL_TIME
                            How often in seconds to poll (60)
      --overscan OVERSCAN   How many readings to average together during the
                            polltime


A systemd unit file is provided for use.  You may want to edit the settings
in the ExecStart line of this file before installing.  Copy to /etc/systemd/system/ and then run systemctl daemon-reload.

## Use with homeassistant

This is my setup, in my sensors.yaml file:

    # garage envirophat
    - platform: mqtt
      name: garage_temperature
      state_topic: merope/envirophat/temperature
      unit_of_measurement: '°C'
    - platform: mqtt
      name: garage_pressure
      state_topic: merope/envirophat/pressure
      unit_of_measurement: 'hPa'
    - platform: mqtt
      name: garage_lux
      state_topic: merope/envirophat/lux
      unix_of_measurement: 'lux'


I run envirophat_mqtt with the following ExecStart:

`ExecStart=/usr/local/bin/envirophat_mqtt --mqtt_host elgafar.garbled.net --mqtt_topic merope/envirophat --mqtt_clientid merope
`

## Making sure it works
Run the following command:
`mosquitto_sub -v -t "#" -h <your MQTT server>`

Watch for messages from the envirophat.

