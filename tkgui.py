from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from os import walk

mypath = "photos/"
image_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    image_list.extend(filenames)
    break
print(image_list)

text_list = image_list
current = 0

def resize(w_box, h_box, pil_image):
    '''
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    '''
    
    w, h = pil_image.size
    f1 = 1.0*w_box/w  # 1.0 forces float division in Python2
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    #print(f1, f2, factor)  # test
    # use best down-sizing filter
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def move(delta):
    global current, image_list
    if not (0 <= current + delta < len(image_list)):
        messagebox.showinfo('End', 'No more image.')
        return
    current += delta
    print('../photos/'+image_list[current])
    photo = ImageTk.PhotoImage(resize(960, 540, Image.open('photos/'+image_list[current]))) #.resize((960,540)))
    
    label['text'] = text_list[current]
    label['image'] = photo
    label.photo = photo


root = Tk()

label = Label(root, compound=TOP)
label.pack()

frame = Frame(root)
frame.pack()

Button(frame, text='Previous picture', command=lambda: move(-1)).pack(side=LEFT)
Button(frame, text='Next picture', command=lambda: move(+1)).pack(side=LEFT)
Button(frame, text='Quit', command=root.quit).pack(side=LEFT)

move(0)

root.mainloop()