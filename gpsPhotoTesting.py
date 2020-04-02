from GPSPhoto import gpsphoto

currentImage = "photos/TestPhoto.JPG"
photo = gpsphoto.GPSPhoto(currentImage)
print(photo.getGPSData())
# Create GPSInfo Data Object
# info = gpsphoto.GPSInfo((38.71615498471598, -9.148730635643007))
# info = gpsphoto.GPSInfo((38.71615498471598, -9.148730635643007), timeStamp='2018:12:25 01:59:05')'''
info = gpsphoto.GPSInfo((20.0, 50.0), alt=83, timeStamp='2018:12:25 01:59:05')

# Modify GPS Data
photo.modGPSData(info, currentImage)

photo2 = gpsphoto.GPSPhoto(currentImage)
print(photo2.getGPSData())
