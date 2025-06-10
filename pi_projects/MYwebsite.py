import network
import socket
from time import sleep
import machine
import rp2
import sys

ssid = ""
password = ''

theLED = machine.Pin("LED",machine.Pin.OUT)
def connectToWifi(): # function to connect to wifi
    wlan = network.WLAN(network.STA_IF) 
    # a network is a set of interconnected devices. 
    #a LAN (local area network) is a set of physically connected devices that can communicate with each other.
    # a WLAN is just a LAN, but now instead of physically connected, they are connected wirelessly
    wlan.active(True) # making the wlan active 
    wlan.connect(ssid, password)   # connecting the wlan to the internet, so it can communicate wirelessly
    while wlan.isconnected() == False:  # if the network is not connected to the wifi, repeat this block of code
        if rp2.bootsel_button() == 1:
            sys.exit()
            theLed.value(1)
            utime.sleep(2)
            theLED.value(0)
        print("Waiting to connect") 
        sleep(1)
    print("Connected!")
    theLED.value(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    return ip

# whats happening now is the rasberry pi is talking to the router, which is talking to the computer 
# when opening a web page, the computer talks the router, which then talks to a port on the server
# then, once the router has made a stable connection with the port, then the webpage info can be sent to the cmoputer 
def open_socket(ip): # creates the socket in the server, where the connection will be made 
    address = (ip, 80) # contains the name of the device the server needs to talk, also includes the port number 
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)  # all this code is just opening up the socket 
    return connection    

def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Mudit Budhdev</title>
    </head>
    <body>

    <h1>Hi!</h1>
    <p>My name is Mudit Budhdev.</p>
    <p>I coded this website using HTML, and host it on my Rasberry Pi Pico 2 W at home.</p>

    </body>
    </html>
    """
    return str(html)

def serve(connection):
        while True:
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            print(request)
            html = webpage()
            client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            client.sendall(html)

            client.close()



ip = connectToWifi()
connection = open_socket(ip)
serve(connection)
