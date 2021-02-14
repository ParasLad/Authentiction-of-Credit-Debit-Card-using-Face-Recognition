# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:58:59 2020

@author: Paras Lad
"""

import tkinter as tk
import cv2,os
import csv
import numpy as np
import pandas as pd
import datetime
import time
#from playsound import playsound
from PIL import ImageTk, Image
from tkinter import scrolledtext
from tkinter import *

def raise_frame(frame):
    frame.tkraise()



root = tk.Tk()
root.geometry('1440x900')
root.title("Debit Card Recognition System")

#root.geometry('1440x900')
root.configure(background='lightblue')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

window = Frame(root)
Page1 = Frame(root)
Page2 = Frame(root)

for frame in(window, Page1, Page2):
    frame.grid(row=0,column=0,sticky='news')
    
message = tk.Label(Page2, text="Online Payment System" ,fg="black"  ,bg="gray91" ,width=58  ,height=1,font=('times', 30, 'italic bold ')) 
message.place(x=0, y=0)

def Payment_page():
    top = tk.Tk()
    top.geometry('1440x900')
    top.title("Payment Portal")
    top.configure(background='lightblue')

    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)
    
    lbl11 = tk.Label(top, text="Withdraw Amount:",width=20  ,height=1  ,fg="black"  ,bg="lightblue" ,font=('times', 20, ' bold ') ) 
    lbl11.place(x=10, y=50)

    txt11 = tk.Entry(top,width=50 ,bg="white" ,fg="black",font=('times', 20, ' bold '))
    txt11.place(x=360, y=50)
    
    #lbl3 = tk.Label(top, text="Data Capture: ",width=20  ,fg="white"  ,bg="saddle brown"  ,height=1 ,font=('times', 20, ' bold ')) 
    #lbl3.place(x=10, y=200)
    
    lbl4 = tk.Label(top, text="Notification : ",width=20  ,fg="black"  ,bg="lightblue"  ,height=1 ,font=('times', 20, ' bold ')) 
    lbl4.place(x=10, y=110)

    message = tk.Label(top, text="" ,bg="white"  ,fg="black"  ,width=70  ,height=2, activebackground = "green") 
    message.place(x=360, y=110)
    message.config(font=("Courier", 13, 'bold'))
    
    message1 = tk.Label(top, text="" ,bg="white"  ,fg="black"  ,width=70  ,height=2, activebackground = "green") 
    message1.place(x=360, y=160)
    message1.config(font=("Courier", 13, 'bold'))
    
    #pa=(txt11.get())

    
    def TrackImages():
        exists = os.path.isfile('Training_ImageLabel/Trainner.yml')
        if exists:
            #recognizer = cv2.face.createLBPHFaceRecognizer()
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            #cv2.createLBPHFaceRecognizer()
            recognizer.read("Training_ImageLabel/Trainner.yml")
            harcascadePath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(harcascadePath)    
            df=pd.read_csv("Customer_Details/Customer_Details.csv")
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX        
            col_names =  ["Customer Id","Customer Name","Card Number","CVV Code","Expiry Month","Expiry Year","Contact Number","Amount"]

            attendance = pd.DataFrame(columns = col_names)  
            while(cam.isOpened()):
                c=0
                ret, im =cam.read()
                if ret:
                    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                    faces=faceCascade.detectMultiScale(gray, 1.3,5)    
                    for(x,y,w,h) in faces:
                        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                        Id, conf = recognizer.predict(gray[y:y+h,x:x+w]) 
                                                     
                        if(conf < 55):
                            #ts = time.time()      
                            #date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                            #timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            global aa 
                            aa=df.loc[df["Customer Id"] == Id,["Customer Name","Card Number","CVV Code","Expiry Month","Expiry Year","Contact Number","Amount"]].values
                            #j=df.set_index('Id','Name','Branch', inplace=True)
                            #print(j)
                            #print("aa:",aa)
                            #branch=aa['Branch']
                            list1 = aa.tolist()
                            #print("branch:",branch)
                            
                            #print(tt)
                            #name=aa['Name']
                            #print(name)
                            #print("name:",name)
                            #name=(", ".join(aa))
                            #tt=str(Id)+"-"+aa
                            #print(type(aa))
                            name=list1[0][0]
                            cardno=list1[0][1]
                            cvvcode=list1[0][2]
                            expmonth=list1[0][3]
                            expyear=list1[0][4]
                            contactno=list1[0][5]
                            amount=list1[0][6]
                            print(amount)
                            print(type(amount))
                            pa=txt11.get()
                            print(pa)
                            print(type(pa))
                            f = float(pa)
                            print(type(f))
                            
                            if(amount>f):
                            
                                amount1=amount-f
                                print(amount1)
                                amount=amount1
                                res = "User Verified"
                                message.configure(text=res)
                                #print(branch)
                                #amount=amount-pa
                            else :
                                c=1
                                res = "You don't have enough balance to pay for this transaction"
                                message.configure(text=res)
                                
                            tt=str(Id)+"-"+name
                            attendance.loc[len(attendance)] = [Id , name,cardno,cvvcode,expmonth,expyear,contactno,amount]
                        else:
                            Id='Unknown'                
                            tt=str(Id)
                            #name=(", ".join(aa))
                        if(conf > 61):
                            #temp=(", ".join(aa))
                            #name=(", ".join(aa))
                            noOfFile=len(os.listdir("Images_Unknown"))+1
                            cv2.imwrite("Images_Unknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])     
                        cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
                    attendance=attendance.drop_duplicates(subset=["Customer Id"],keep='last')
                    #print(attendance)
                    cv2.imshow('im',im) 
                if (cv2.waitKey(1)==ord('q')):
                    break
            #ts = time.time()      
            #date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            #timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            #Hour,Minute,Second=timeStamp.split(":")
            fileName="Fetch_Data/Data.csv"
            attendance.to_csv(fileName,index=False)
            fileName1="Customer_Details/Customer_Details.csv"
            attendance.to_csv(fileName1,index=False)
            cam.release()
            cv2.destroyAllWindows()
            if(Id=='Unknown'):
                res = "Payment Unsuccessful"
            elif(c==1):
                res = "Payment Unsuccessful"
            else:    
                res = "Payment Successful"#+",".join(str(f) for f in Id)
            message1.configure(text= res)
            #playsound('thankyou.mp3')
            #print(attendance)
            attendance = attendance.to_string(index=False)
            res=attendance
            S = Scrollbar(top)
            T = Text(top,state='disabled',height=6, width=120)
            T.configure(state='normal')
            T.place(x=200,y=500)
            S.config(command=T.yview)
            T.config(yscrollcommand=S.set)
            #message2.configure(text= res)
            T.insert(END, res)
            T.configure(state='disabled')
        else:
            res = "Data not available for tracking"
            message.configure(text= res)
    
    
    
    
    trackImg = tk.Button(top, text="PAY", command=TrackImages  ,fg="Black"  ,bg="lightgreen"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    trackImg.place(x=200, y=300)
    quitWindow = tk.Button(top, text="Quit", command=top.destroy  ,fg="Black"  ,bg="lightgreen"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    quitWindow.place(x=830, y=300)
    
    copyWrite = tk.Text(top, background=top.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
    copyWrite.tag_configure("superscript", offset=10)
    copyWrite.configure(state="disabled",fg="red"  )
    copyWrite.pack(side="left")
    copyWrite.place(x=800, y=750)
    
    top.mainloop()

def Register_page():
    top = tk.Tk()
    top.geometry('1440x900')
    top.title("Register Portal")
    top.configure(background='lightgreen')

    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)
    
    lbl = tk.Label(top, text="Customer ID",width=20  ,height=1  ,fg="Black"  ,bg="lightgreen" ,font=('times', 20, ' bold ') ) 
    lbl.place(x=10, y=50)

    txt = tk.Entry(top,width=30 ,bg="white" ,fg="black",font=('times', 20, ' bold '))
    txt.place(x=360, y=50)

    lbl2 = tk.Label(top, text="Customer Full Name",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl2.place(x=10, y=120)

    txt2 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt2.place(x=360, y=120)

    lbl8 = tk.Label(top, text=" Contact number",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl8.place(x=10, y=190)

    txt8 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt8.place(x=360, y=190)

    lbl4 = tk.Label(top, text="Debit/Credit Card Number",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl4.place(x=10, y=260)

    txt4 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt4.place(x=360, y=260)


    lbl5 = tk.Label(top, text=" CVV code",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl5.place(x=10, y=330)

    txt5 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt5.place(x=360, y=330)
    
    lbl7 = tk.Label(top, text=" Expiry year",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl7.place(x=10, y=400)

    txt7 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt7.place(x=360, y=400)
    
    lbl6 = tk.Label(top, text="Expiry month",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl6.place(x=10, y=470)

    txt6 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt6.place(x=360, y=470)
    
    lbl9 = tk.Label(top, text=" Amount",width=20  ,fg="Black"  ,bg="lightgreen"    ,height=1 ,font=('times', 20, ' bold ')) 
    lbl9.place(x=10, y=540)

    txt9 = tk.Entry(top,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
    txt9.place(x=360, y=540)


    lbl3 = tk.Label(top, text="Notification : ",width=20  ,fg="Black"  ,bg="lightgreen"  ,height=1 ,font=('times', 20, ' bold ')) 
    lbl3.place(x=10, y=610)

    message = tk.Label(top, text="" ,bg="white"  ,fg="black"  ,width=42  ,height=2, activebackground = "green") 
    message.place(x=360, y=610)
    message.config(font=("Courier", 13, 'bold'))
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        
        return False
    
    def TakeImages(): 
        if (len(txt.get()) != 0) and (len(txt2.get()) != 0):
            Id=(txt.get())
            name=(txt2.get())
            cardno =(txt4.get())
            cvvcode = (txt5.get())
            expmonth =(txt6.get())
            expyear =(txt7.get())
            contactno =(txt8.get())
            amount =(txt9.get())
            print(cvvcode)
            final=name.replace(" ", "")
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("Training_Image/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
               #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
               # break if the sample number is morethan 100
                elif sampleNum>50:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Student Id : " + Id +"    " " Name : "+ name
            row = [Id , name,cardno,cvvcode,expmonth,expyear,contactno,amount]
            with open('Customer_Details/Customer_Details.csv','a+') as csvFile:
               writer = csv.writer(csvFile)
               writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
          #else:
             #   if(Id.isalpha()):
             #       res = "Please enter numeric student id"
              #      message.configure(text= res)
               # elif(is_number(name)):
                #    res = "Please enter alphabetical name of student"
                 #   message.configure(text= res)
                #else:
                 #   print("")
        else:
            res = "Please enter full data of customer to proceed further"
            message.configure(text= res)  
    def Validate():
        Id=(txt.get())
        name=(txt2.get())
        cardno =(txt4.get())
        cvvcode = (txt5.get())
        expmonth =(txt6.get())
        expyear =(txt7.get())
        contactno =(txt8.get())
        amount =(txt9.get())
        print(cvvcode)
        final=name.replace(" ", "")
        l=len(cardno)
        l1=len(cvvcode)
        l2=len(expyear)
        l3=len(contactno)
        if(Id.isalpha()):
            res = "Enter correct Id"
            message.configure(text= res)
        elif(is_number(final)):
            res = "Enter correct name"
            message.configure(text=res)
        elif(cardno.isalpha()):
            res = "Card no. should not be in alphabet. Please enter correct card no."
            message.configure(text=res)
        elif(l>16 or l<16):
            res = "Card no. should be of 16 digit. Please enter correct card no."
            message.configure(text=res)
        elif(l1>3 or l1<3):
            res = "Cvv should be of 3 digits. Please enter correct cvv no."
            message.configure(text=res)
        elif(l2!=4):
            res = "Please enter 4 digit exp year"
            message.configure(text=res)
        elif(l3!=10):
            res = "Please enter 10 digit contact number"
            message.configure(text=res)
        elif(expmonth=='1'):
            res = "Data Validated"
            message.configure(text=res)
          
        elif(expmonth=='2'):
            res = "Data Validated"
            message.configure(text=res)
        elif(expmonth=='3'):
            res = "Data Validated"
            message.configure(text=res)
            
        elif(expmonth=='4'):
            res = "Data Validated"
            message.configure(text=res)
           
        elif(expmonth=='5'):
            res = "Data Validated"
            message.configure(text=res)
           
        elif(expmonth=='6'):
            res = "Data Validated"
            message.configure(text=res)
           
        elif(expmonth=='7'):
            res = "Data Validated"
            message.configure(text=res)
            
        elif(expmonth=='8'):
            res = "Data Validated"
            message.configure(text=res)
            
        elif(expmonth=='9'):
            res = "Data Validated"
            message.configure(text=res)
            
        elif(expmonth=='10'):
            res = "Data Validated"
            message.configure(text=res)
            
        elif(expmonth=='11'):
            res = "Data Validated"
            message.configure(text=res)
           
        elif(expmonth=='12'):
            res = "Data Validated"
            message.configure(text=res)
           
        else:
            res = "Please enter the correct month"
            message.configure(text=res)
    
                    
    
    def TrainImages():
        if  os.listdir('Training_Image') :
            # Store configuration file values
            #print("File is present")
            #recognizer = cv2.face_LBPHFaceRecognizer.create()
            recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            faces,Id = getImagesAndLabels("Training_Image")
            recognizer.train(faces, np.array(Id))
            recognizer.write("Training_ImageLabel/Trainner.yml")
            res = "Image Trained"#+",".join(str(f) for f in Id)
            message.configure(text= res)             
        else:
            res = "Data not available for training "
            message.configure(text= res)         
 
    from PIL import Image
    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #print(imagePaths)
        
        #create empth face list
        faces=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)  
        return faces,Ids
    
    takeImg = tk.Button(top, text="Validate data", command=Validate  ,fg="black"  ,bg="coral"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    takeImg.place(x=950, y=50)
    takeImg = tk.Button(top, text="Take Images", command=TakeImages  ,fg="black"  ,bg="coral"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    takeImg.place(x=950, y=210)
    trainImg = tk.Button(top, text="Train Images", command=TrainImages  ,fg="black"  ,bg="coral"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    trainImg.place(x=950, y=370)
    quitWindow = tk.Button(top, text="Quit", command=top.destroy  ,fg="black"  ,bg="coral"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
    quitWindow.place(x=950, y=530)
        
    top.mainloop()
    

from tkinter import *
from PIL import Image, ImageTk

Page2.configure(background='gray91')

image = Image.open("Logo.png")
photo = ImageTk.PhotoImage(image)

label = Label(image=photo)
label.image = photo
label.place(x=500, y=100)

Label(Page2).pack()
b1 =tk.Button(Page2, text="Pay", command=Payment_page  ,fg="black"  ,bg="gold"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
b2 = tk.Button(Page2, text="Register", command=Register_page  ,fg="black"  ,bg="gold"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))

b1.place(x=300 ,y=550)

b2.place(x=710 ,y=550)

message = tk.Label(Page2, text="" ,bg="gray91"  ,fg="black"  ,width=20  ,height=28, activebackground = "green" ,wraplength=200) 
message.place(x=0, y=100)
message.config(font=("Courier", 13, 'bold'))

message1 = tk.Label(Page2, text="" ,bg="gray91"  ,fg="black"  ,width=20  ,height=28, activebackground = "green" ,wraplength=200 ) 
message1.place(x=1150, y=100)
message1.config(font=("Courier", 13, 'bold'))

res = " Be Aware Of \n Phising attacks   \n                          Our system does not ask for the details of your account like /PIN/ Password/ mobile numbers etc. Therefore any one pretending to be asking you for information may be fraudulent entities   "

message.configure(text=res)

res1 = "For any inquiry about our system, you can approach our nearest branch in your ciy              \n In case any unauthorized access to your information, accounts or disputed transactions, using Face Detection service, please visit our branch at your earliest or contact us on email:ops@gmail.com or contact-1236543985"

message1.configure(text=res1)

root.mainloop()