# coding: utf8
# Created by: Virgile Mison
# Created for: Original project for ECBM 4040 (Columbia University) for cropping and resize pictures of bottle
# Used for preprocessing images for Neural Nets training set

from PIL import Image
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import PIL
from tkinter import filedialog
import os
import math

def fit(w1,h1,w2,h2):
    # fit image of size w1,h1 in window of size w2,h2
    # outuput : new size of image and ratio
    ratio = min(w2/w1,h2/h1)
    return int(w1*ratio), int(h1*ratio), ratio

def getXYinImage(x, y):
    # get coordinate of click from event.x, event.y and send back in the coordinate system of image, plus if the click is inside or outside image.
    return x, y, (w_image*(1-paddingThreshold)>x  and x>w_image*paddingThreshold and h_image*(1-paddingThreshold)>y and y>h_image*paddingThreshold)

def position_resize_to_origin(x,y,ratio):
    # transform coordinate to different ratio
    return [x/ratio, y/ratio]

def recenter_points(p1,p2):
    # from p1 and p2 top & down point on bottle, get center of bottle and height of bottle
    return [int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2)],int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))

class App(Frame):
    # Tkinter GUI to select 2 points on bottle
    def __init__(self, master):
        Frame.__init__(self, master)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.image = ImageTk.PhotoImage(original)
        self.display = Canvas(self, bd=0, highlightthickness=1,width=800,height=800)
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        self.display.grid(row=0, sticky=W+E+N+S)
        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize)
        self.bind_all("<Button-1>", self.callback)
        w_image,h_image,r_image = 800,800,1
        self.mainloop()


    def resize(self, event):
        global w_image,h_image,r_image
        size = (event.width, event.height)
        w_image,h_image,r_image = fit(original.size[0],original.size[1],size[0],size[1])
        image = original.resize((w_image, h_image),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
        # Make reappear older points
        for j in range(0,i):
            x = points[j][0]*r_image
            y = points[j][1]*r_image
            self.display.delete("pt"+str(j))
            self.display.create_oval(x-3, y-3, x+3, y+3, fill="red",tags="pt"+str(j))

    def callback(self, event):
        global i, points
        x,y,inside = getXYinImage(event.x,event.y)
        if inside:
            self.display.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="red", tags="pt"+str(i))
            points.append(position_resize_to_origin(x,y,r_image))
            i+=1
            if i>1:
                self.quit()

def crop(namefile,percentageExtra,reduceSize=64,showResult=True):
    global original, paddingThreshold, i, points
    i=0
    points=[]
    paddingThreshold = 0.05     # threshold for border to recognize pointer in image -> in order to resize the window without selecting a point
    original = Image.open(namefile)
    root = Tk()
    root.title("Bottle selection "+str(n)+"/"+str(l))
    Label(root,text="Click on the top and bottom of the bottle").pack()
    root.wm_attributes("-topmost", 1)
    root.focus_force()
    app = App(root)
    print ("2 points selected, GUI stopped")
    root.destroy()

    # Cropping and resizing image
    centerBottle, hBottle = recenter_points(points[0],points[1])
    correctedHeight = hBottle*(1+percentageExtra)/2
    cropped = original.crop((centerBottle[0]-correctedHeight, centerBottle[1]-correctedHeight, centerBottle[0]+correctedHeight, centerBottle[1]+correctedHeight)).resize((reduceSize,reduceSize), PIL.Image.ANTIALIAS)

    # Showing result if asked
    if showResult:
        cropped.show()
    # Save new image
    new_name = "_".join(namefile.split('_')[0:3])+"_"+str(reduceSize)+"x"+str(reduceSize)+"_"+namefile.split('_')[4].split('.')[0]

    directory = os.path.dirname(os.path.abspath(__file__))+'/resized'
    if not os.path.exists(directory):           # create new directory if needed
        os.makedirs(directory)
    cropped.save(directory+'/'+new_name +".png")

# define variables
percentageExtra = 0.1       # percentage of extra height to consider for the bottle
reduceSize = 64             # size of reduced image : reduceSize*reduceSize


root1 = Tk()
root1.withdraw()
root1.update()
# ask for files to crop (for now only in the same directory)
filez = filedialog.askopenfilenames(title='Choose a file')
files = root1.tk.splitlist(filez)
print(filez)
root1.destroy()

namefiles=[f.split('/')[-1] for f in files]
n=0
l=len(namefiles)
for namefile in namefiles:
    n+=1
    crop(namefile,percentageExtra,reduceSize,showResult=True)
