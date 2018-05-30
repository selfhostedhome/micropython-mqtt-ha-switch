from umqtt.simple import MQTTClient
import machine
import utime
import ubinascii

LED = machine.Pin(2, machine.Pin.OUT, value=0)

CLIENT = None
SERVER = "192.168.1.9"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
COMMAND_TOPIC = "home/office/switch1/set"
STATE_TOPIC = "home/office/switch1"
AVAILABILITY_TOPIC = "home/office/switch1/available"


def new_msg(topic, msg):

    print(msg)

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

    print("Connected to %s, subscribed to %s topic" % (SERVER, COMMAND_TOPIC))

    try:
        while 1:
            CLIENT.wait_msg()
    finally:
        CLIENT.publish(AVAILABILITY_TOPIC, "offline")
        CLIENT.disconnect()

main()
