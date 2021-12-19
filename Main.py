from tkinter import *
from tkinter import messagebox
import collectdata
tkWindow = Tk()  

#กำหนดขนาดจอ
tkWindow.geometry('900x400+550+200')  
tkWindow.title('Bigdata Analysis')
frame = Frame(tkWindow)

collectData = StringVar()
Num = IntVar()

#ใช้เรียก collecttweet หลังจากกดปุ่ม submit
def textto():
    message = collectData.get()
    count = Num.get()
    allTweet = collectdata.collecttweet( message, count)
    collectdata.wordcloudThai(allTweet)

#ปุ่ม submit    
button = Button(tkWindow,
    text = 'Submit',
    command = textto)
button.place(x=450,y=200)

#กำหนดกล่องกรอกข้อความ
Entry(tkWindow,textvariable=collectData,width=60,).place(x=250,y=100)
Entry(tkWindow,textvariable=Num,width=60,).place(x=250,y=150)

#กำหนดข้อความ
keyword = Label(text="Hashtag",font=24).place(x=150,y=100)
keyword = Label(text="document",font=24).place(x=150,y=150)

tkWindow.mainloop()