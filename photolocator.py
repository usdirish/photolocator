import exifread
import requests
import os.path



#separate images out that do not have gps data
# def checkGPSinfo(image):
    # f = exifread()


#open the image for viewing (allow multiple images to get the same data, for instance all on the same date,likely in the same place)
keyFile = open(os.path.dirname(__file__) + '/../key.txt')
key = keyFile.readline()
locAddress = input("Where did this picture get taken? (Address or Business): ") or ""
locCityState = (input("What city and state? :") or "San Diego, CA").replace(" ","+")
response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={locAddress},+{locCityState}&key={key}')

resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])