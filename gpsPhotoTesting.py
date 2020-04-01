from GPSPhoto import gpsphoto
photo = gpsphoto.GPSPhoto("photos/TestPhoto.JPG")

# Create GPSInfo Data Object
# info = gpsphoto.GPSInfo((38.71615498471598, -9.148730635643007))
# info = gpsphoto.GPSInfo((38.71615498471598, -9.148730635643007), timeStamp='2018:12:25 01:59:05')'''
info = gpsphoto.GPSInfo((38.71615498471598, -9.148730635643007), alt=83, timeStamp='2018:12:25 01:59:05')

# Modify GPS Data
photo.modGPSData(info, 'new_photo.jpg')