#! /usr/bin/python3

import argparse
import json
import time

import paho.mqtt.client as mqtt

DEVICE_NAME = "led-01"
DOC_TOPIC = "$hw/events/device/" + DEVICE_NAME + "/twin/update/document"
UPDATE_TOPIC = "$hw/events/device/" + DEVICE_NAME + "/twin/update"

DELAY = 10

power = "INIT"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(DOC_TOPIC)
    print("Subscribe: " + DOC_TOPIC)


def on_disconnect(client, userdata, flag, rc):
    print("Disonnected with result code " + str(rc))


def on_message(client, userdata, msg):
    global power
    updates = json.loads(str(msg.payload.decode("utf-8")))
    power_cur = updates["twin"]["power"]["current"]["expected"]["value"]
    print("Received desired power status: " + power_cur)
    if power != power_cur:
        power = power_cur
        print("Changed actual power status: " + power)
        msg = {"twin": {"power": {"actual": {"value": power}}}}
        print("Reporting actual power status. Wait for {} sec.".format(str(DELAY)))
        time.sleep(DELAY)
        client.publish(UPDATE_TOPIC, json.dumps(msg))
        print("Reported")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker", help="mqtt broker ip")
    args = parser.parse_args()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(args.broker, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
