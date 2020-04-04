import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
import urllib.request

from tensorflow.python.keras.models import load_model
classifier=load_model("batch_size-1000 epoch-50.h5")
#classifier=load_model("epoch =60 batch-size=100, reduced more some neurons.h5")
from tensorflow.keras.preprocessing import image
import numpy as np

root=tk.Tk()
root.title("Cat vs Dog")
root.geometry("725x430")
root.resizable(0,1)

title_label=tk.Label(root,text="Image Classification",font=("Segoe UI Black",30))
title_label.pack()

frame1=tk.LabelFrame(root,padx=10,pady=10)
frame1.pack()

class image_selector:
    img_path='cat2.jpg'


def file_select():
    """
    Files can be selected

    Returns
    -------
    None.

    """
    global image_display_label,img,imag
    img_loc=filedialog.askopenfilename(title="Select image of cat or dog",filetypes=(("Image files","*jpg"),("All Files","*.*")))
    print(img_loc)
    basewidth = 200
    img = Image.open(img_loc)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    imag = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img=ImageTk.PhotoImage(imag)
    img_select.img_path=img_loc
    image_display_label['image']=img  
    display_label['text']=""
                        
info_disp_label=tk.Label(frame1,text="""You can select the image file from the Disk or you can copy-paste the image url in the text box and press the Fetch button.""")
info_disp_label.grid(row=0,column=0,columnspan=3)

img_select=image_selector()
img_select_button=tk.Button(frame1,text="Select Image From Disk",command=file_select)
img_select_button.grid(row=1,column=0)

or_label=tk.Label(frame1,text="or")
or_label.grid(row=1,column=1)

url=tk.StringVar()
url_entry=tk.Entry(frame1,textvariable=url,width=70)
url_entry.grid(row=1,column=2)

def url_image_fetch():
    global image_display_label,img,imag

    url_link=url.get()
    print(url_link)
    img = Image.open(urllib.request.urlopen(url_link))
    img.save("down.jpg")
    basewidth = 200
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    imag = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img=ImageTk.PhotoImage(imag)
    img_select.img_path="down.jpg"

    image_display_label['image']=img
    url.set("")
    display_label['text']=""


fetch_button=tk.Button(frame1,text="Fetch",command=url_image_fetch)
fetch_button.grid(row=1,column=3)

frame2=tk.LabelFrame(root,padx=10,pady=10)
frame2.pack(fill='x')


imag=Image.open(img_select.img_path)
imag=imag.resize((200,200),Image.ANTIALIAS)
img=ImageTk.PhotoImage(imag)

image_display_label=tk.Label(frame2,image=img)
image_display_label.grid(row=0,column=0,padx=30)

def predict():
    loc=img_select.img_path
    img = image.load_img(loc, target_size=(64, 64,3))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = classifier.predict(images)
    classes=classes.flatten().tolist()
    print(classes[0])
    display_label['text']=str(classes[0])
    if classes[0]>.5:
        display_label['text']="I am a Dog"
        disp_res_image['image']=dog_img_tk
    else:
        display_label['text']="I am a Cat"
        disp_res_image['image']=cat_img_tk




predict_button=tk.Button(frame2,text="Predict",command=predict)
predict_button.grid(row=0,column=1,padx=60)

cat_img=Image.open("cat_vector.jpg")
cat_img_tk=ImageTk.PhotoImage(cat_img)

dog_img=Image.open("dog_vector.png")
dog_img_tk=ImageTk.PhotoImage(dog_img)

disp_res_image=tk.Label(frame2,image=cat_img_tk)
disp_res_image.grid(row=0,column=2,padx=30)

frame3=tk.Frame(root,padx=10,pady=10)
frame3.pack()

display_label=tk.Label(frame3,text="I am a Cat",font=("Segoe UI Black",20))
display_label.pack()

root.mainloop()


