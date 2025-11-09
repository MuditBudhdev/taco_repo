import requests
import time
import cv2


def takePhoto():
    cam = cv2.VideoCapture(0)
    temp, frame = cam.read()
    cv2.imwrite("pic.jpg", frame)
    cam.release()
    cv2.destroyAllWindows()


token_url = "https://opensky-network.org/api/oauth/token"
client_id = "muditbudhdev-api-client"
client_secret = "txJfJpwnS5MjmCWFdcJjxJIL3NyofYsy"
token_response = requests.post(token_url,data = {"grant_type" : "client_credentials"}, auth = (client_id, client_secret))
token = token_response.json().get("access_token")
url = 'https://opensky-network.org/api/states/all'


params = {
    "lamin": 37.299951,   
    "lomin": -122.023914, 
    "lamax": 37.300419,   
    "lomax": -122.023071
}
# instructions to determine params
# paramters are just the bouding box in which you are scanning
# lamin and lomin are the bottom right
# lamax and lomax are top left
# set this up, then switch lomin and lomax values


headers = {"Authorization":f"Bearer {token}"}
while True:
    time.sleep(2)
    responses = requests.get(url, params = params, headers = headers)
    try:
        num_planes = len(responses.json()["states"]) # calling the API and then parsing the output into a dictionary
        # gives an output one 1. time (time data was collected) 2. states (a list of lists, each list containg info about a plane)
        states = responses.json()["states"]
        plane_code = states[0][1]
        print("Num planes near house: " + f"{num_planes}")
        print("The first plane callsign is: " + f"{plane_code}")
        takePhoto()
        # insert code here to send to google drive

    except Exception as e:
        print("there are no planes near house")




