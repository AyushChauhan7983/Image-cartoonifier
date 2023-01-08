import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)

top = tk.Tk()
top.geometry('600x600')
top.title('Cartoonify Your Image')
top.configure(background='white')
label = Label(top,background='#CDCDCD', font = ('calibri',20,'bold'))
C = Canvas(top, bg = "blue", height = 600, width = 600)
coord = 10, 50, 240, 210

image2 =Image.open('C:\\Users\\dell\\Desktop\\sample pictures\\bg_image.jpg')
image1 = ImageTk.PhotoImage(image2)
image_1 = C.create_image(200.0, 300.0, image = image1)

C.create_text(100.0, 50.0, anchor="nw", text="Cartoonify your image\n", fill="#1345D6", font=("anybody",30,'bold'))

frame = Frame(bg = "white")
image3 = Image.open('C:\\Users\\dell\\Desktop\\sample pictures\\image.jpg')
frame.picture = ImageTk.PhotoImage(image3)
frame.label = Label(frame, image=frame.picture)
frame.label.pack()
C.create_window(25,230, anchor = NW, window = frame, width = 550, height = 350)

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5,borderwidth = 5)
upload.configure(background='#FF5733', foreground='white',font=('anybody',10,'bold'))
upload.pack(side=TOP,pady=50)
upload.place(x=215, y=120)
C.pack()

def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (960, 540))

    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))

    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges and highlighting for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))

    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))

    # Plotting the whole transition throughout the process
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save cartoon image",command=lambda: save(ReSized6, ImagePath),padx=30,pady=5,borderwidth = 5)
    save1.configure(background='#0096FF', foreground='white',font=('anybody',10,'bold'))
    save1.pack(side=TOP,pady=50)
    save1.place(x=195, y=170)
    plt.show()

def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

top.mainloop()



