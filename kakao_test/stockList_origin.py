

"""
1. Top 50
2. PER 30% 미만
3. PBR 5 미만
4. ROE 10 이상
5. 3개월 / 1년 / 3년
"""
import csv
import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd

# import sys
# sys.stdout = open('naver_stock_1to50.txt', 'w')

# Total_Message = []
stockList = []

PER_BASE = 30
PBR_BASE = 5
ROE_BASE = 10

Request_Count = 0


def getDataOfParam(stock_dict, param):

    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param}).get_text().strip()

    #param 에 매핑되는 row 검색 => 상위 이동 => 해당 row의 모든 td 컬럼 가져오기
    dataOfParam = sub_tbody.find("th", attrs = {"class":param}).parent.find_all("td")

    stock_dict[sub_title] = [i.get_text().strip() for i in dataOfParam]

    return stock_dict

    """for idx, value in enumerate(dataOfParam):

        temp_data = value.get_text().strip()

        stockone[sub_title] = {'part': temp_str}


        if not temp_data:
            continue

        # print(stock_name, temp_str, idx, temp_data)
        stockone[idx]= temp_data
        temp_data = temp_data.replace(",", "")

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

    # return stock_message
    return stockone"""

Total_Message = []

for page_num in range(1,5):

    url = "https://finance.naver.com/sise/sise_market_sum.nhn?page="+"%d"%(page_num)

    # print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    stock_head = soup.find("thead").find_all("th")
    data_head = [head.get_text() for head in stock_head]
    data_head.pop()

    stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    stockTop50_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})
    result_str = ""

    data_header = ['회사명']

    for idx, stock in enumerate(stockTop50_corp):
        corp_Message = []
        stock_dict = dict()

        stock_dict['name'] =stock.get_text()
        stock_dict['link'] = "https://finance.naver.com/"+stock["href"]

        flag = 1

        sub_res = requests.get(stock_dict['link'])
        sub_soup = BeautifulSoup(sub_res.text, 'lxml')

        sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})
        if sub_thead is not None:
            sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col"})
        else:
            continue
        """ 위 코드로 return None 값에 대한 예외처리
        
        if str(stock_name).find("KO2DEX") >= 0 or \
                        str(stock_name).find("맥쿼리인프라") >= 0 or \
                        str(stock_name).find("TIGER") >= 0 or \
                        str(stock_name).find("롯데리츠") >= 0 or \
                        str(stock_name).find("티와이홀딩스") >= 0 or \
                        str(stock_name).find("제이알글로벌리츠") >= 0 or \
                        str(stock_name).find("200") >= 0:

                    continue
                """
        ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
        # ParamList = ['ROE(지배주주)', 'PER(배)', 'PBR(배)']

        for idx, pText in enumerate(ParamList):

            if sub_soup.find('strong', text=pText) is not None:
                param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
            else:
                continue
            """ 위 코드로 return None 값에 대한 예외처리"""

            param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
            # print (param)
            # result_message = getDataOfParam(idx, stock_link, stock_name, param)

            stock_dict = getDataOfParam(stock_dict, param)

        #이미지 링크 추가
        img_link_list = ['month3', 'year', 'year3']
        img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

        for img in img_link_list:
            stock_dict['img_'+img] = img_link.replace("day", img)

        stockList.append(stock_dict)
        print(stockList[len(stockList) - 1])

"""
            corp_Message.extend(result_message)
            if len(result_message) != 0 :
                temp = result_message.pop()
                if temp.startswith("@@"):
                    flag = 0
                    # img1 = img_link.replace("day", img_link_list[0])
                    # img2 = img_link.replace("day", img_link_list[1])
                    # img3 = img_link.replace("day", img_link_list[2])
                    # Total_Message.append(temp)
                    # Total_Message.append(img1)
                    # Total_Message.append(img2)
                    # Total_Message.append(img3)

                    break



        if flag == 0:

            continue

        if corp_Message:
            Request_Count += 1
            Total_Message.append("<a href='"+stock_link+"'>"+ stock_name+"</a>")
            Total_Message.extend(corp_Message)
            img1 = img_link.replace("day", img_link_list[0])
            img2 = img_link.replace("day", img_link_list[1])
            img3 = img_link.replace("day", img_link_list[2])
            Total_Message.append("<br>[3개월]<br><img src='"+img1+"'>")
            Total_Message.append("[1년]<br><img src='"+img2+"'>")
            Total_Message.append("[3년]<br><img src='"+img3+"'>")
            Total_Message.append("")

        # writer.writerow(stock_name)
        # writer.writerow(result_str)
        # print(stock_name)
        # print(result_str)
        break
"""

# print("\n".join(Total_Message))

# E-mail 전송
"""
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

id = '1004gmyoul@naver.com'
password = 'qhdksdls!2'
sendEmail = '1004gmyoul@naver.com'
today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
subject = '['+today+' 주식추천 종목]-'+str(Request_Count)+'개 회사'
text = "<br>".join(Total_Message)
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
"""