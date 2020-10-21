
def sendMail(message):
    import smtplib, os
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime

    id = '1004gmyoul@naver.com'
    password = 'qhdksdls!2'
    sendEmail = '1004gmyoul@naver.com'
    today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    subject = '[' + today + ' 주식추천 종목]-' + str(Request_Count) + '개 회사'
    text = "<br>".join(message)
    addrs = ['1004gmyoul@naver.com', 'gy.ryu@lotte.net']  # send mail list

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


def getDataOfParam(index, stock_name, param):

    data_body = []

    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param})
    temp_str = sub_title.get_text().strip()

    data_body.append(stock_name)
    data_body.append(temp_str)

    data = sub_tbody.find("td")
    # data_body.append(data.get_text().strip()+"?")

    data1 = sub_tbody.find("th", attrs = {"class":param})
    data2 = data1.next_element.next_element.next_element.next_element
    data_body.append(data2.get_text().strip())

    # index : 0:매출, 1:영업이익, 2:당기순이익, 3:ROE, 4:PER, 5:PBR
    # idx : 0~3 : 연간실적, 4~9 : 최근 분기 실적

    stock_message=[]

    # print (stock_name, index, data2.get_text().strip())

    for idx, value in enumerate(data2.find_next_siblings()):

        # print(idx)
        temp_data = value.get_text().strip()
        if not temp_data:
            continue

        if index == 0 and idx==7 :
            if float(temp_data) > float(ROE_BASE):
                s = "# ROE_BASE:{} 달성 => {}".format( ROE_BASE, float(temp_data))
                stock_message.append(s)
                # print(s)
            else:
                s = "@@ [{}] - ROE_BASE:{} 미달성 - {}".format(stock_name, ROE_BASE, float(temp_data))
                stock_message.clear()
                stock_message.append(s)
                break

        elif index == 1 and idx==7 :
            if float(temp_data) < float(PER_BASE):
                s = "# PER_BASE:{} 달성 => {}".format( PER_BASE, float(temp_data))
                stock_message.append(s)
                # print(s)
            else:
                s = "@@ [{}] - PER_BASE:{} 미달성 - {}".format(stock_name, PER_BASE, float(temp_data))
                stock_message.clear()
                stock_message.append(s)
                break

        elif index == 2 and idx==7 :
            if float(temp_data) < PBR_BASE:
                s = "# PBR_BASE: {} 달성 => {}".format( PBR_BASE, float(temp_data))
                stock_message.append(s)
                # print(s)
            else:
                s = "@@ [{}] - PBR_BASE:{} 미달성 - {}".format(stock_name, PBR_BASE, float(temp_data))
                stock_message.clear()
                stock_message.append(s)
                break

        # data_body.append(temp_data)

    return stock_message
    # print(data_header)
    # print(data_body)

# filename = "naver_stock_1to200.csv"
# f = open(filename, "w", encoding="utf-8-sig", newline='')
# writer = csv.writer(f, delimiter='\t')
