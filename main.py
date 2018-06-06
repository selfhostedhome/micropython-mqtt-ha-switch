from umqtt.simple import MQTTClient
import machine
import utime
import ubinascii

from config import SERVER, COMMAND_TOPIC, STATE_TOPIC, AVAILABILITY_TOPIC

LED = machine.Pin(2, machine.Pin.OUT, value=1)

CLIENT = None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())


def new_msg(topic, msg):

    print("Received {}".format(msg))

    if msg == b"on":
        LED.value(0)
        CLIENT.publish(STATE_TOPIC, "on")
    elif msg == b"off":
        LED.value(1)
        CLIENT.publish(STATE_TOPIC, "off")


def main():
    global CLIENT
    CLIENT = MQTTClient(CLIENT_ID, SERVER)
    CLIENT.set_callback(new_msg)
    CLIENT.connect()

    CLIENT.subscribe(COMMAND_TOPIC)

    # Publish as available once connected
    CLIENT.publish(AVAILABILITY_TOPIC, "online")

    print("Connected to {}, subscribed to {} topic".format(SERVER, COMMAND_TOPIC))

    try:
        while 1:
            CLIENT.wait_msg()
    finally:
        CLIENT.publish(AVAILABILITY_TOPIC, "offline")
        CLIENT.disconnect()

main()
