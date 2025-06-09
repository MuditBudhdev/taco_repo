import utime
import machine

led_pin = machine.Pin("LED", machine.Pin.OUT)

while True:
    led_pin.value(1)
    utime.sleep(1)
    led_pin.value(0)
    utime.sleep(1)

    print("It works!")