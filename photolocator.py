import exifread
import pprint
import csv
import pandas
import requests
import os.path
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from GPSPhoto import gpsphoto

mypath = "photos/"
image_list = []
complete_list = []
current = 0
outputFile = open("output.csv", 'w')
w = csv.writer(outputFile)
completeGPSfiles = open('GPSCompletedImages.txt','a')

pp = pprint.PrettyPrinter(indent=4)



#with the image open, read exif data. If there is no gps data, put it in the gui, if there is gps data, add it to the list of complete photos
def checkGPS(image):
    #f = open(image, 'rb')
    tags = exifread.process_file(image)
    w.writerow(['name*******************************************************',image])
    # for tag in tags.keys():
    #     if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
    #         w.writerow([tag,tags[tag]])
    for key, val in tags.items():
        if key in ('GPS GPSLatitude'):    
            print('**' + currentImage)
            return False
    return False

def addGPSTags(curLat, curLong):
    photo = gpsphoto.GPSPhoto(currentImage)
    rawDataBefore = gpsphoto.getRawData(currentImage)
    w.writerow(['name*******************************************************BEFORE', currentImage])
    for tag in rawDataBefore.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            w.writerow([tag,rawDataBefore[tag]])
    info = gpsphoto.GPSInfo((curLat, curLong))
    photo.modGPSData(info, currentImage)
    rawDataAfter = gpsphoto.getRawData(currentImage)
    w.writerow(['name*******************************************************AFTER', currentImage])
    for tag in rawDataAfter.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            w.writerow([tag,rawDataAfter[tag]])
    


#make the image a regular size to fit the GUI
def resize(w_box, h_box, pil_image):
    w, h = pil_image.size
    f1 = 1.0*w_box/w
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

#function to flip through the images in the GUI
def move(delta):
    global current, image_list, currentImage
    if not (0 <= current + delta < len(image_list)):
        messagebox.showinfo('End', 'No more image.')
        return
    current += delta
    imgStr = 'photos/' + image_list[current]
    currentImage = imgStr
    print("74 the image is: " + imgStr)
    img =  Image.open(imgStr)
    photo = ImageTk.PhotoImage(resize(960, 540, img))    
    label['text'] = image_list[current]
    label['image'] = photo
    label.photo = photo
    

#obtain lat/long from Google api
def getLocation(loc1="5408 Jamestown Rd", loc2="San Diego, CA"):
    #get the api key from the key.txt file in the parent directory of PhotoLocator
    keyFile = open(os.path.dirname(__file__) + '/../key.txt')
    key = keyFile.readline()
    locAddress = loc1.replace(" ","+")
    locCityState = loc2.replace(" ","+")
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={locAddress},+{locCityState}&key={key}')
    resp_json_payload = response.json()
    return (float(resp_json_payload['results'][0]['geometry']['location']['lat']), float(resp_json_payload['results'][0]['geometry']['location']['lng']))
                
def callback(*args):
    val1 = e1.get()
    val2 = e2.get()
    print(f'{val1} and {val2}')
    curLat, curLong = getLocation(val1, val2)
    print(f'{curLat}, {curLong}')
    addGPSTags(curLat, curLong)
    move(+1)


#GUI 
root = Tk()
root.title('PhotoLocator')
windowHeight = 650
windowWidth = 730
root.geometry(f'{windowWidth}x{windowHeight}')
label = Label(root, compound=TOP)
frame = Frame(root)

#ask the questions:
q1 = Label(root, text="Where was this picture taken? (Business or Address)")
q2 = Label(root, text="What city? (Defaults to San Diego)")
e1 = Entry(root, justify = CENTER)
e2 = Entry(root, justify = CENTER)
e2.insert(0, "San Diego, CA")
b1 = Button(root,text='Submit', command=callback)
b2 = Button(root, text='Previous picture', command=lambda: move(-1))
b3 = Button(root, text='Next picture', command=lambda: move(+1))
b4 = Button(root, text='Quit', command=root.quit)

q1.grid(row=1, column = 0,sticky=W)
q2.grid(row=2, column = 0,sticky=W)
e1.grid(row=1, column=1,sticky=W+E)
e2.grid(row=2, column=1,sticky=W+E)
b1.grid(row=1,column=2,rowspan=2, sticky=N+S+E+W)
b2.grid(row=3, column=0, sticky=N+S+E+W)
b3.grid(row=3, column=1, sticky=N+S+E+W)
b4.grid(row=3, column=2, sticky=N+S+E+W)
frame.grid(row=4,column = 0, columnspan = 3)
label.grid(row=5,column = 0, columnspan = 3)
root.bind('<Return>', callback)

def main():
    global currentImage
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for x in filenames:
            if x[-3:].upper() == "JPG" or x[-4:].upper() == "JPEG":
                currentImage = mypath + x
                f = open(currentImage, 'rb')
                if not checkGPS(f):
                    image_list.append(x)
                else:
                    with open("GPSCompletedImages.txt", "a") as file_object:
                        file_object.write(x + '\n')
    pp.pprint(image_list)    
    move(0)
    root.mainloop()
    outputFile.close()

if __name__ == '__main__':
    main()