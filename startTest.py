import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8"
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
res = requests.get(url, verify=False)
soup = BeautifulSoup(res.text, "lxml")

location = soup.find("span", attrs={"class":"btn_select"}).get_text()
current_degree = soup.find("span", attrs={"class":"todaytemp"}).get_text()
dosee = soup.find("span", attrs={"class":"tempmark"}).get_text().replace("도씨", "")
cast_txt = soup.find("p", attrs={"class":"cast_txt"}).get_text()

indicator = soup.find("dl", attrs={"class":"indicator"}).get_text()
indicator = indicator.split()

print_str = "<a href='https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8'>[오늘의 날씨]</a>\
<img src<br/><br/>위치 : {}".format(location)+\
            "<br/>{}".format(cast_txt)+\
            "<br/>현재 {}{}".format(current_degree, dosee)+"<br/>"
print("[오늘의 날씨]")
print("위치 : {}".format(location))
print("{}".format(cast_txt))
print("현재 {}{}".format(current_degree, dosee))
print()



for idx in range(0, 6, 2):
    print(indicator[idx].strip()+" "+indicator[idx+1].strip())
    print_str += indicator[idx].strip()+" "+indicator[idx+1].strip()+"<br/>"


import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

id = '1004gmyoul@naver.com'
password = 'qhdksdls!2'
sendEmail = '1004gmyoul@naver.com'
subject = '[오늘의 날씨]'
text = print_str
addrs = ['1004gmyoul@naver.com', 'godshy1611@naver.com']  # send mail list

# login
smtp = smtplib.SMTP('smtp.naver.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login(id, password)

for addr in addrs:
    # message
    message = MIMEMultipart()
    message.attach(MIMEText(text, 'html'))

    # Send
    message["From"] = sendEmail
    message["To"] = addr
    message['Subject'] = subject
    smtp.sendmail(sendEmail, addr, message.as_string())

smtp.quit()


# import smtplib
# from email.mime.text import MIMEText
#
# def sendMail(me, you, msg):
#     smtp = smtplib.SMTP_SSL('smtp.naver.com', 587)
#     smtp.login(me, 'qhdksdls!2')
#     msg = MIMEText(msg)
#     msg['Subject'] = 'TEST'
#     smtp.sendmail(me, you, msg.as_string())
#     smtp.quit()
#
# sendMail('1004gmyoul@naver.com', 'gy.ryu@lotte.net', '메일보내기')


#-*- coding: utf-8 -*-
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# msg = MIMEText('메일 본문')                   # 메일 본문 첨부
# msg['Subject'] = Header('메일 제목', 'utf-8') # 메일 제목 첨부
# msg['From'] = 'gmyoul@gmail.com'       # 송신 메일
# msg['To'] = 'gy.ryu@lotte.net'        # 수신 메일
# with smtplib.SMTP_SSL('smtp.gmail.com') as smtp: # (*)
#  smtp.login('gmyoul@gmail.com','qhdksdls!2')           # (**)
#  smtp.send_message(msg)

#
# import os, copy
# import smtplib
# from string import Template
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
#
# class EmailHTMLContent:
#     """e메일에 담길 컨텐츠"""
#
#     def __init__(self, str_subject, template, template_params):
#         """string template과 딕셔너리형 template_params받아 MIME 메시지를 만든다"""
#         assert isinstance(template, Template)
#         assert isinstance(template_params, dict)
#         self.msg = MIMEMultipart()
#
#         # e메일 제목을 설정한다
#         self.msg['Subject'] = str_subject  # e메일 제목을 설정한다
#
#         # e메일 본문을 설정한다
#         str_msg = template.safe_substitute(**template_params)  # ${변수} 치환하며 문자열 만든다
#         mime_msg = MIMEText(str_msg, 'html')  # MIME HTML 문자열을 만든다
#         self.msg.attach(mime_msg)
#
#     def get_message(self, str_from_email_addr, str_to_eamil_addrs):
#         """발신자, 수신자리스트를 이용하여 보낼메시지를 만든다 """
#         mm = copy.deepcopy(self.msg)
#         mm['From'] = str_from_email_addr  # 발신자
#         mm['To'] = ",".join(str_to_eamil_addrs)  # 수신자리스트
#         return mm
#
# class EmailSender:
#     """e메일 발송자"""
#
#     def __init__(self, str_host, num_port=25):
#         """호스트와 포트번호로 SMTP로 연결한다 """
#         self.str_host = str_host
#         self.num_port = num_port
#         self.ss = smtplib.SMTP(host=str_host, port=num_port)
#         # SMTP인증이 필요하면 아래 주석을 해제하세요.
#         self.ss.starttls() # TLS(Transport Layer Security) 시작
#         self.ss.login('gmyoul@gmail.com', 'knlkclpdgyprkkfs') # 메일서버에 연결한 계정과 비밀번호
#
#     def send_message(self, emailContent, str_from_email_addr, str_to_eamil_addrs):
#         """e메일을 발송한다 """
#         cc = emailContent.get_message(str_from_email_addr, str_to_eamil_addrs)
#         self.ss.send_message(cc, from_addr=str_from_email_addr, to_addrs=str_to_eamil_addrs)
#         del cc
#
# str_host    = 'smtp.gmail.com'
# num_port    = 587 # SMTP Port
# emailSender = EmailSender(str_host, num_port)
#
# str_subject = 'hello' # e메일 제목
# template = Template("""<html>
#                             <head></head>
#                             <body>
#                                 Hi ${NAME}.<br>
#                                 This is a test message.
#                             </body>
#                         </html>""")
# template_params = {'NAME':'Son'}
# emailHTMLContent = EmailHTMLContent(str_subject, template, template_params)
#
# str_from_email_addr = 'gmyoul@gmail.com' # 발신자
# str_to_eamil_addrs  = ['gy.ryu@lotte.net'] # 수신자리스트
# emailSender.send_message(emailHTMLContent, str_from_email_addr, str_to_eamil_addrs)