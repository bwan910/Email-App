from tkinter import *
import os
import csv
import time
from tkinter import filedialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from tkinter import messagebox
from pathlib import Path

count, c = 0, 0
creds = 'tempfile.temp'  # this just sets the creds to 'tempfile.temp'


def mail():
    def clear():
        input_email_from.delete(0, "end")
        input_password.delete(0, "end")
        input_email_to.delete(0, "end")
        input_subject.delete(0, "end")
        textBox.delete('1.0', "end")
        file.destroy()

    def attach():
        global count
        count += 1
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        path = Path(root.filename)
        file = Label(root, text=path.name)
        file.grid(row=7, column=0, sticky=W)

    def Pass():
        pass

    def Sendmail():
        global count
        global c
        msg = MIMEMultipart()
        msg['From'] = input_email_from.get()
        msg['To'] = input_email_to.get()
        msg['Subject'] = input_subject.get()

        body = textBox.get("1.0", "end-1c")

        msg.attach(MIMEText(body, 'plain'))
        if count > 0:
            filename = root.filename
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename="+filename)
            msg.attach(part)
        else:
            pass
        text = msg.as_string()
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(input_email_from.get(), input_password.get())

        try:
            mail.sendmail(input_email_from.get(), msg['To'], text)
            c += 1
            print('email sent')
        except:
            print('error sending email')

        mail.quit()
        if c >= 1:

            messagebox.showinfo("Successfully", "Email Sent")

        else:
            messagebox.showinfo("Error", "Fail to sent")

    def mutiple():
        Sendmail()
        clear()

    root = Tk()
    root.geometry('1000x1000')
    root.title("Sending Email")

    # Making the filemenu
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Exit", command=root.quit)

    # Label for email from
    lbl_email_from = Label(root, text='Email From:', font=('Arial', 16))
    lbl_email_from.place(x=200, y=100)

    # Input box for email from
    input_email_from = Entry(root, bd=2, font=('Arial', 12), width=40)
    input_email_from.place(x=400, y=100)

    # Label for password
    lbl_password = Label(root, text="Password:", font=('Arial', 16))
    lbl_password.place(x=200, y=200)

    # Input box for password
    input_password = Entry(root, bd=2, font=('Arial', 12), show="*", width=40)
    input_password.place(x=400, y=200)

    # Label for Email to
    lbl_email_to = Label(root, text="Email to:", font=('Arial', 16))
    lbl_email_to.place(x=200, y=300)

    # Input box for Email to
    input_email_to = Entry(root, bd=2, font=('Arial', 12), width=40)
    input_email_to.place(x=400, y=300)

    # Label for subject
    lbl_subject = Label(root, text="Subject:", font=('Arial', 16))
    lbl_subject.place(x=200, y=400)

    # Input box for Email to
    input_subject = Entry(root, bd=2, font=('Arial', 12), width=40)
    input_subject.place(x=400, y=400)

    # Textbox
    textBox = Text(root, height=10, width=100)
    textBox.place(x=100, y=500)

    # Send Button
    btn_send = Button(root, text="Send Email", font=(
        'Bold', 18), bg="Yellow", command=mutiple)
    btn_send.place(x=830, y=300)

    btn_attachment = Button(root, text="Insert Files",
                            font=('Bold', 15), command=attach)
    btn_attachment.place(x=300, y=700)

    root.mainloop()


mail()
