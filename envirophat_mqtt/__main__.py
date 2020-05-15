#!/usr/bin/env python3
"""
I'm really only interested in the temp/pressure/lux readings. The rest could
be easily added, but I don't care.
"""

import argparse
import time
from envirophat import light, weather, leds
import paho.mqtt.client as mqtt


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_host', help='MQTT host',
                        default='localhost', type=str, action='store')
    # parser.add_argument('--mqtt_user', help='MQTT username',
    #                     default=None, type=str, action='store')
    # parser.add_argument('--mqtt_pass', help='MQTT password',
    #                     default=None, type=str, action='store')
    parser.add_argument('--mqtt_topic', help='MQTT topic',
                        default='envirophat', type=str, action='store')
    parser.add_argument('--mqtt_clientid', help='MQTT client ID',
                        default='pi', type=str, action='store')
    parser.add_argument('--mqtt_port', help='MQTT port',
                        default=1883, type=int, action='store')
    parser.add_argument('--poll_time', type=int, action='store',
                        default=60,
                        help='How often in seconds to poll (60)')
    parser.add_argument('--overscan', type=int, action='store',
                        default=5,
                        help='How many readings to average together during the polltime')

    args = parser.parse_args()
    return args


def gather_env_data(args):
    data = {}

    lux = 0
    temp = 0
    press = 0
    for loop in range(args.overscan):
        lux += light.light()
        print("real lux={0}".format(lux))
        temp += weather.temperature()
        press += weather.pressure() / 100.0

        if (args.overscan > 1):
            time.sleep(float(args.poll_time) / args.overscan)

    data['lux'] = round(lux / args.overscan, 1)
    data['temperature'] = round(temp / args.overscan, 1)
    data['pressure'] = round(press / args.overscan, 1)

    return data


def main(args=None):
    args = parse_arguments()

    leds.off()
    print('Envirophat MQTT starting up')

    try:
        client = mqtt.Client(client_id=args.mqtt_clientid)
        client.connect(host=args.mqtt_host, port=args.mqtt_port)
    except Exception as e:
        print("Failed to start MQTT client, abort: {0}".format(str(e)))
        return 1

    client.loop_start()

    while(True):
        data = gather_env_data(args)
        # print(f"lux = {data['lux']}")
        # print(f"temp = {data['temperature']}")
        # print(f"pres = {data['pressure']}")
        for key in data.keys():
            try:
                client.publish(f"{args.mqtt_topic}/{key}", f"{data[key]}")
            except Exception as e:
                print("Unable to publish topic, aborting. {0}".format(str(e)))
                return 1


if __name__ == "__main__":
    main()
