from tkinter import *
import test
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Word cloud from keyword in twiter")

running = False

#กำหนดข้อความ keyword
keyword = Label(text="Keyword",font=24).place(x=150,y=50)

#กล่องใส่ keyword
def click(event):
    mytextkeyword.configure(state=NORMAL)
    mytextkeyword.delete(0, END)

textkeyword = StringVar()
mytextkeyword = Entry(root,textvariable=textkeyword,width=60,)
mytextkeyword.insert(0, "enter the keyword")
mytextkeyword.configure(state=DISABLED)
mytextkeyword.bind("<Button-1>",click)
mytextkeyword.place(x=250,y=50)
collectData = IntVar()

#สั่งให้ส่ง keyword ไป run ใน test.py
def print_text():
    if running:
        message = textkeyword.get()
        print(message)
        #collData = collectData.get()
        # print(running)

        #กำหนดข้อความ อัพโหลดรูปภาพ
        keyword = Label(text="อัพโหลดรูปภาพ",font=24).place(x=150,y=150)
        #เพิ่มรูปภาพ
        image = Image.open("C:/KMITL/P3T1/Big data/Project/tweepy/img/love.jpg")
 
        # Resize the image using resize() method
        resize_image = image.resize((150, 150))
 
        img = ImageTk.PhotoImage(resize_image)
 
        # create label and add resize image
        label1 = Label(image=img)
        label1.image = img
        label1.place(x=300,y=150)
    root.after(1000,print_text)
    #else: 
       # print("stop")


#สั่งส่ง keyword ไป
def start():
    global running 
    running = True

#สั่งหยุด(ได้แค่ใน File เดียวกันเท่านั้น)
def stop():
    global running
    running = False

#btn_text = StringVar()
#ใส่ปุ่ม start
starts = Button(root,text="start", command=start,width=10,bg="black",fg="white").place(x=650,y=45)
stops = Button(root,text="stop", command=stop,width=10,bg="black",fg="white").place(x=750,y=45)
#btn_text.set("a")



#กำหนดข้อความ collecd data
keyword = Label(text="collecd data",font=24).place(x=150,y=100)

#กล่องใส่ collecd data
mytextcollecdData = Entry(root,textvariable=collectData,width=60,).place(x=250,y=100)

#กำหนดข้อความ document
keyword = Label(text="document",font=24).place(x=650,y=95)

#กำหนดขนาดจอ
root.geometry("900x400+550+200")
#สั่งรันหา keyword
root.after(1000, print_text)

#สั่งรัน Tk
root.mainloop()