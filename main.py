from tkinter import *
from tkinter import ttk
from functools import partial
from typing import Any, Union

from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
import pyqrcode
import png
from pyqrcode import QRCode
import cv2
from pyzbar.pyzbar import decode
import tempfile
import os
global total_amount
total_amount=[]

def mainscreen() :
    # for connection between the server and application
    def connect_server():
        username = usernameEntry.get()
        password = passwordEntry.get()
        try:
            global mydb #declaring mydb as a global variable
            mydb = mysql.connector.connect(host='localhost', user=username, password=password, database="department")
            if(mydb):
                a = messagebox.askquestion("connection established", "username and password matched sucessfully, Are you want to continue ? ")
        except:
            b = messagebox.showerror("connection failed ", "username and password not matched")
        if(a=='yes'):
            mainscreen.destroy()
            optionscreen()


    mainscreen = Tk()
    # window configuration
    mainscreen.geometry('1536x700')
    mainscreen.minsize(1440, 848)
    mainscreen.configure(bg='lightgray')
    mainscreen.title("QR-BILLING SYSTEM")
    p1 = PhotoImage(file='qrlogo.png')
    mainscreen.iconphoto(False, p1)

    # menu configuration
    mymenu = Menu(mainscreen)
    mymenu.add_command(label="FILE")
    mymenu.add_command(label="HELP")
    mainscreen.configure(menu=mymenu)

    # making logo and logo_text
    image = Image.open("qrlogo.png")
    resize_image = image.resize((100, 100))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=380, y=20)
    # ------------------------------------------------------------------------
    logo_text = Label(text="QR-BILL GENERATING SYSTEM", font=('Bold', 30,), fg='white', bg='lightgray')
    logo_text.place(x=500, y=40)

    w = Canvas(mainscreen, width=1490, height=10, bg="darkgray")
    w.place(x=20, y=170)


    # making entry and text widget & button
    usernameLabel = Label(mainscreen, text="User Name :", font=('Bold', 20,), fg='black', bg='lightgray')
    usernameLabel.place(x=490, y=300)
    usernameEntry = Entry(mainscreen, font=('Bold', 20,))
    usernameEntry.place(x=720, y=300)
    passwordLabel = Label(mainscreen, text="Password   :", font=('Bold', 20,), fg='black', bg='lightgray')
    passwordLabel.place(x=490, y=370)
    passwordEntry = Entry(mainscreen, show='*', font=('Bold', 20,))
    passwordEntry.place(x=720, y=370)
    # ------------------------------------------------------------------------------------
    loginButton = Button(mainscreen, text="Login",command=connect_server,font=('Bold', 15,),fg="cyan",bg="red").place(x=750, y=450)  # command nessasary

    # bottom widget text
    bottom_text = Label(mainscreen, text="Copyrighted & created by ankit jha ece-batch ABES EC", font=('Bold', 10,),
                        fg="black", bg="lightgray")
    bottom_text.place(x=20, y=740)
    bottom_text2 = Label(mainscreen, text="* * For any information mail us", font=('Bold', 10,), fg="black",
                         bg="lightgray")
    bottom_text2.place(x=1300, y=740)

    mainscreen.mainloop()

def optionscreen():
    def command_1():
        optionscreen.destroy()
        addproduct()

    def command_2():
        optionscreen.destroy()
        billingproduct()

    optionscreen = Tk()

    # window configuration
    optionscreen.geometry('1536x700')
    optionscreen.minsize(1440, 848)
    optionscreen.configure(bg='lightgray')
    optionscreen.title("QR-BILLING SYSTEM")
    p1 = PhotoImage(file='qrlogo.png')
    optionscreen.iconphoto(False, p1)

    # menu configuration
    mymenu = Menu(optionscreen)
    mymenu.add_command(label="Hello!")
    mymenu.add_command(label="Hello!")
    optionscreen.configure(menu=mymenu)

    # making logo and logo_text
    image = Image.open("qrlogo.png")
    resize_image = image.resize((100, 100))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=380, y=20)
    # ------------------------------------------------------------------------
    logo_text = Label(text="QR-BILL GENERATING SYSTEM", font=('Bold', 30,), fg='white', bg='lightgray')
    logo_text.place(x=500, y=40)

    # bottom widget text
    bottom_text = Label(optionscreen, text="Copyrighted & created by ankit jha ece-batch ABES EC", font=('Bold', 10,),
                        fg="black", bg="lightgray")
    bottom_text.place(x=20, y=740)
    bottom_text2 = Label(optionscreen, text="* * For any information mail us", font=('Bold', 10,), fg="black",
                         bg="lightgray")
    bottom_text2.place(x=1300, y=740)

    #canvs ---> for vertical line
    w = Canvas(optionscreen,width=10,height=600,bg="darkgray")
    w.place(x=755,y=150)

    #two button
    b1 = Button(optionscreen, text="Add new product and generate QR-CODE",command=command_1,font=('Bold', 15,),fg="cyan").place(x=200, y=350)
    b1_text=Label(text="* * for adding new product detail ",font=('Bold',10),fg="red",bg="lightgray").place(x=200, y=400)
    b2 = Button(optionscreen, text="Generate bill using QR-CODE",command=command_2,font=('Bold', 15,),fg="green").place(x=950, y=350)
    b2_text = Label(text="* * for generating a new bill using tags ", font=('Bold', 10), fg="red", bg="lightgray").place(x=950, y=400)

    optionscreen.mainloop()

def addproduct():
    def adddetail():
        mycursor = mydb.cursor()
        pcode = productcode_entry.get()
        pname = productname_entry.get()
        pmin = productmin_entry.get()
        pprice = productprice_entry.get()
        if(pcode and pname and pmin and pprice):
            try:
                url = pyqrcode.create(pcode)
                url.png(pname, scale=6)
                query = "INSERT INTO  products (product_code ,product_name ,min_quantity ,price) VALUES(%s,%s,%s,%s)"
                my_data = (pcode, pname, pmin, pprice)
                mycursor.execute(query, my_data)# insert data
                messagebox.showinfo("Entry saved successfully","Product details added succesfully ")
                mydb.commit()
            except:
                messagebox.showerror("Entry already exist", "following entry already exist in record")
        else:
            messagebox.showerror("Invalid entry","Entry cannot be blank")
    def backscreen():
        addproduct.destroy()
        optionscreen()


    addproduct = Tk()

    # window configuration
    addproduct.geometry('1536x700')
    addproduct.minsize(1440, 848)
    addproduct.configure(bg='lightgray')
    addproduct.title("QR-BILLING SYSTEM")
    p1 = PhotoImage(file='qrlogo.png')
    addproduct.iconphoto(False, p1)

    # menu configuration
    mymenu = Menu(addproduct)
    mymenu.add_command(label="Hello!")
    mymenu.add_command(label="Hello!")
    addproduct.configure(menu=mymenu)

    # making logo and logo_text
    image = Image.open("qrlogo.png")
    resize_image = image.resize((100, 100))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=380, y=20)
    # ------------------------------------------------------------------------
    logo_text = Label(text="QR-BILL GENERATING SYSTEM", font=('Bold', 30,), fg='white', bg='lightgray')
    logo_text.place(x=500, y=40)

    # canvs ---> for vertical line
    w = Canvas(addproduct, width=1490, height=10, bg="darkgray")
    w.place(x=20, y=170)

    # bottom widget text
    bottom_text = Label(addproduct, text="Copyrighted & created by ankit jha ece-batch ABES EC", font=('Bold', 10,),
                        fg="black", bg="lightgray")
    bottom_text.place(x=20, y=740)
    bottom_text2 = Label(addproduct, text="* * For any information mail us", font=('Bold', 10,), fg="black",
                         bg="lightgray")
    bottom_text2.place(x=1300, y=740)

    #all entry labels and text labels
    productcode_label = Label(addproduct, text="Product Code     :", font=('Bold', 20,), fg='black', bg='lightgray').place(x=460,y=220)
    productname_label = Label(addproduct, text="Product name     :", font=('Bold', 20,), fg='black', bg='lightgray').place(x=460,y=320)
    productmin_label = Label(addproduct, text="Product  min       :", font=('Bold', 20,), fg='black', bg='lightgray').place(x=460,y=420)
    productprice_label = Label(addproduct, text="Product price      :", font=('Bold', 20,), fg='black', bg='lightgray').place(x=460,y=520)
    #---------------------------------------------------------------------------------------------------------------
    productcode_entry = Entry(addproduct, font=('Bold', 20,))
    productcode_entry.place(x=760,y=220)
    productname_entry = Entry(addproduct, font=('Bold', 20,))
    productname_entry.place(x=760,y=320)
    productmin_entry = Entry(addproduct, font=('Bold', 20,))
    productmin_entry.place(x=760,y=420)
    productprice_entry = Entry(addproduct, font=('Bold', 20,))
    productprice_entry.place(x=760,y=520)

    #---------------------------------------------------------------------------------------------------------------
    loginButton = Button(addproduct, text="ADD Record And Generate QR-CODE",command=adddetail, font=('Bold', 15,),fg="cyan").place(x=600,y=620)  # command nessasary
    back_button = Button(addproduct,text="Back",font=('Bold',15),fg="cyan",bg="red",command=backscreen).place(x=1300,y=220)

def billingproduct():
    def qrscaning():
        cap = cv2.VideoCapture(0)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            # detect and decode
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image
            if data:
                a = data
                break
            cv2.imshow("QRCODEscanner", img)
            if cv2.waitKey(1) == ord("q"):
                break
        #data is in a-->variable(product_code)
        cap.release()
        cv2.destroyAllWindows()

        #search recrod in database using a-->varaiable
        mycursor = mydb.cursor()
        try:
            quary = "SELECT * FROM products where product_code = '" + a + "'"
            mycursor.execute(quary)
            details = mycursor.fetchone()
            # variable --> detail having a tuple of all details of variable a
            textarea.insert(END, f"\n{details[0]}\t\t\t{details[1]}\t\t\t\t{details[2]}\t\t\t{details[3]}\n")
            total_amount.append(details[3])
        except:
            messagebox.showerror("RECORD NOT FOUND", "Following object not found in products data")

    def printbill():
        textarea.insert(END,f"-----------------------------------------------------------------------------------------------------------------------------------------")
        textarea.insert(END,f"\n\t\t\t\t\tTotal amount :--\t\t\t\t\t{sum(total_amount)}\n")
        total_amount.clear()
        q=textarea.get(1.0,"end-1c")
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,'print')

    def resetarea():
        textarea.delete(1.0, END)
        textarea.insert(END, f"\t\t\t\tDEPARTMENTAL STORE pvt.ltd\n")
        textarea.insert(END, f"\t\t\tRohini west sector-25 ,New Delhi, 202002 , 19002304056\n")
        textarea.insert(END,
                        f"-----------------------------------------------------------------------------------------------------------------------------------------")
        textarea.insert(END, f"\nPRODUCT CODE\t\t\tPRODUCT NAME\t\t\t\tMIN QUANTITY\t\t\tPRICE\n")
        textarea.insert(END,
                        f"-----------------------------------------------------------------------------------------------------------------------------------------")

    def backscreen():
        billingproduct.destroy()
        optionscreen()


    billingproduct = Tk()

    # window configuration
    billingproduct.geometry('1536x700')
    billingproduct.minsize(1440, 848)
    billingproduct.configure(bg='lightgray')
    billingproduct.title("QR-BILLING SYSTEM")
    p1 = PhotoImage(file='qrlogo.png')
    billingproduct.iconphoto(False, p1)

    # menu configuration
    mymenu = Menu(billingproduct)
    mymenu.add_command(label="Hello!")
    mymenu.add_command(label="Hello!")
    billingproduct.configure(menu=mymenu)

    # making logo and logo_text
    image = Image.open("qrlogo.png")
    resize_image = image.resize((100, 100))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img
    label1.place(x=380, y=20)
    # ------------------------------------------------------------------------------------------
    logo_text = Label(text="QR-BILL GENERATING SYSTEM", font=('Bold', 30,), fg='white', bg='lightgray')
    logo_text.place(x=500, y=40)

    # canvs ---> for vertical line
    w = Canvas(billingproduct, width=1490, height=10, bg="darkgray")
    w.place(x=20, y=150)

    #-------------bill area----------------------------------------------------------------------
    F2=Frame(billingproduct,relief=GROOVE,bd=10)
    F2.place(x=80,y=180,width=1000,height=550)
    bill_title=Label(F2,text='Receipt',font='arial 15 bold',bd=7,relief=GROOVE).pack(fill=X)
    scrol_y=Scrollbar(F2,orient=VERTICAL)
    scrol_y.pack(side=RIGHT,fill=Y)
    textarea=Text(F2,font='arial 15',yscrollcommand=scrol_y.set)
    textarea.pack(fill=BOTH)
    scrol_y.config(command=textarea.yview)
    textarea.insert(END,f"\t\t\t\tDEPARTMENTAL STORE pvt.ltd\n")
    textarea.insert(END,f"\t\t\tRohini west sector-25 ,New Delhi, 202002 , 19002304056\n")
    textarea.insert(END,f"-----------------------------------------------------------------------------------------------------------------------------------------")
    textarea.insert(END,f"\nPRODUCT CODE\t\t\tPRODUCT NAME\t\t\t\tMIN QUANTITY\t\t\tPRICE\n")
    textarea.insert(END,f"-----------------------------------------------------------------------------------------------------------------------------------------")




    #-------------------button------------------------------------------------------------------
    printButton = Button(billingproduct, text="Print Receipt ", font=('Bold', 20,),fg="cyan",command=printbill).place(x=1200,y=240)
    resetButton = Button(billingproduct, text="Reset Screen", font=('Bold', 20,),fg="red",command=resetarea).place(x=1200,y=400)
    additembutton = Button(billingproduct, text="  Add items   ",font=('Bold', 20),fg="cyan",command=qrscaning).place(x=1200,y=550)
    back_button = Button(billingproduct, text="Back", font=('Bold', 15), fg="cyan", bg="red",command=backscreen).place(x=1255, y=670)

    billingproduct.mainloop()


#---------------------------------- main function -----------------------------------------------
if __name__ == '__main__':
    mainscreen()
#------------------------------------------------------------------------------------------------