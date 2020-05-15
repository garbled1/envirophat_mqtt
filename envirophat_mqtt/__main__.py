#!/usr/bin/env python3
"""
I'm really only interested in the temp/pressure/lux readings. The rest could
be easily added, but I don't care.
"""

import argparse
import time
from envirophat import light, weather


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtt_host', help='MQTT host',
                        default='localhost', type=str, action='store')
    parser.add_argument('--mqtt_user', help='MQTT username',
                        default=None, type=str, action='store')
    parser.add_argument('--mqtt_pass', help='MQTT password',
                        default=None, type=str, action='store')
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
                        help='How many readings to average together')

    args = parser.parse_args()
    return args


def gather_env_data(args):
    data = {}

    lux = 0
    for loop in range(args.overscan):
        lux += light.light()

        if (args.overscan > 1):
            time.sleep(float(args.poll_time) / args.overscan)

    data['lux'] = lux / args.overscan

    return data


def main(args=None):
    args = parse_arguments()

    while(True):
        data = gather_env_data(args)
        print(f"lux = {data['lux']}")


if __name__ == "__main__":
    main()
