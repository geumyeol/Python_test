

"""
1. Top 50
2. PER 30% 미만
3. PBR 5 미만
4. ROE 10 이상
5. 3개월 / 1년 / 3년
"""
# E-mail Library
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import csv
import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd

from beautifultable import BeautifulTable

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

"""
PER_BASE = 20
PBR_BASE = 3
ROE_BASE = 15
"""
def printRecommendedItems(stock):

    # print(stock['name'])
    numberPER = 0
    numberPBR = 0
    numberROE = 0

    resultString = ""

    # print(stock)
    dataHeader = ['실적', '2017.12','2018.12','2019.12','2020.12(E)','2019.06','2019.09','2019.12','2020.03','2020.06','2020.09(E)']
    for idx in range(4, 9):
        if stock['ROE(지배주주)'][idx] is None or not stock['ROE(지배주주)'][idx] or\
            stock['PER(배)'][idx] is None or not stock['PER(배)'][idx] or\
            stock['PBR(배)'][idx] is None or not stock['PBR(배)'][idx] :
            # print(idx)
            continue
        if float(stock['ROE(지배주주)'][idx].replace(",","")) > ROE_BASE:
            numberROE += 1
        if float(stock['PER(배)'][idx].replace(",","")) > PER_BASE:
            numberPER += 1
        if float(stock['PBR(배)'][idx].replace(",","")) > PBR_BASE:
            numberPBR += 1

        if numberROE >= 2 and numberPER >= 2 and numberPBR >= 2:


            resultString += "<a href = '"+stock['link']+"'> "+str(stock['idx'])+". "+stock['name']+"</a> - 현재가 : "+stock['curCost']
            resultString += "<table border='1px'><tr><td>"+"<td>".join(dataHeader)+"</tr>"
            resultString += "<br><tr><td>매출액<td>"+"<td>".join(stock['매출액'])+"</tr>"
            resultString += "<br><tr><td>당기순이익<td>" + "<td>".join(stock['당기순이익'])+"</tr>"
            resultString += "<br><tr><td>ROE<td>" + "<td>".join(stock['ROE(지배주주)'])+"</tr>"
            resultString += "<br><tr><td>PER<td>" + "<td>".join(stock['PER(배)'])+"</tr>"
            resultString += "<br><tr><td>PBR<td>" + "<td>".join(stock['PBR(배)'])+"</tr></table>"
            resultString += "<br><br><br>[3개월]<br><img src='" + stock['img_month3']+"'>"
            resultString += "<br><br>[1년]<br><img src='" + stock['img_year']+"'>"
            resultString += "<br><br>[3년]<br><img src='" + stock['img_year3']+"'>"

            # print(resultString)
            return 1, resultString

        else:
            continue

    return 0, ""

def sendEmailfunc(text):
    id = '1004gmyoul@naver.com'
    password = 'qhdksdls!2'
    sendEmail = '1004gmyoul@naver.com'
    today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    subject = '[' + today + ' 주식추천 종목]-' + str(Request_Count) + '개 회사'
    addrs = ['1004gmyoul@naver.com']  # send mail list

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

Total_message = ''

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

    data_header = ['회사명']

    for index, stock in enumerate(stockTop50_corp):
        corp_Message = []
        stock_dict = dict()

        stock_dict['name'] =stock.get_text()
        stock_dict['idx'] = index
        stock_dict['link'] = "https://finance.naver.com/"+stock["href"]

        flag = 1

        sub_res = requests.get(stock_dict['link'])
        sub_soup = BeautifulSoup(sub_res.text, 'lxml')

        cur_cost = sub_soup.find("div", attrs={"class":"rate_info"}).find("div", attrs={"class":"today"}).\
            find("p", attrs={"class":"no_today"}).get_text().strip().split()
        # print("cur_cost", cur_cost[0], "##")
        stock_dict['curCost'] = cur_cost[0]

        sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})
        if sub_thead is not None:
            sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col"})
        else:
            continue
        """ 위 코드로 return None 값에 대한 예외처리"""


        ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
        # ParamList = ['ROE(지배주주)', 'PER(배)', 'PBR(배)']

        for idx, pText in enumerate(ParamList):

            if sub_soup.find('strong', text=pText) is not None:
                param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
            else:
                stock_dict.clear()
                flag = 0
                break
            """ 위 코드로 return None 값에 대한 예외처리"""

            param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
            # print (param)
            # result_message = getDataOfParam(idx, stock_link, stock_name, param)

            stock_dict = getDataOfParam(stock_dict, param)

        if flag == 1:
            #이미지 링크 추가
            img_link_list = ['month3', 'year', 'year3']
            img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

            for img in img_link_list:
                stock_dict['img_'+img] = img_link.replace("day", img)

            returnFlag, resultStr = printRecommendedItems(stock_dict)

            if returnFlag == 1:
                Request_Count += 1
                Total_message += resultStr+"<br>"
    print("==Complete 50 Corp==")

sendEmailfunc(Total_message)
print(Total_message)


