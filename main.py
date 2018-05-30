import machine
import utime

led = machine.Pin(0, machine.Pin.OUT)

while True:
    led.off()
    utime.sleep(1)
    led.on()
    utime.sleep(1)
