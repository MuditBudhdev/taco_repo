import machine
import utime

theLED = machine.Pin("LED", machine.Pin.OUT)

theLED.value(1)      # LED ON
utime.sleep(1)       # wait 1 second
theLED.value(0)      # LED OFF
print("i am running")
