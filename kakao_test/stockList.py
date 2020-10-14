

"""
1. Top 50
2. PER 30% 미만
3. PBR 5 미만
4. ROE 10 이상
5. 3개월 / 1년 / 3년
"""
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# import sys
# sys.stdout = open('naver_stock_1to50.txt', 'w')
Total_Message = []

PER_BASE = 30
PBR_BASE = 5
ROE_BASE = 10

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
                s = "## [{}] - ROE_BASE:{} 달성 - {}".format(stock_name, ROE_BASE, float(temp_data))
                stock_message.append(s)
                # print(s)
            else:
                s = "@@ [{}] - ROE_BASE:{} 미달성 - {}".format(stock_name, ROE_BASE, float(temp_data))
                stock_message.clear()
                stock_message.append(s)
                break

        elif index == 1 and idx==7 :
            if float(temp_data) < float(PER_BASE):
                s = "## [{}] - PER_BASE:{} 달성 - {}".format(stock_name, PER_BASE, float(temp_data))
                stock_message.append(s)
                # print(s)
            else:
                s = "@@ [{}] - PER_BASE:{} 미달성 - {}".format(stock_name, PER_BASE, float(temp_data))
                stock_message.clear()
                stock_message.append(s)
                break

        elif index == 2 and idx==7 :
            if float(temp_data) < PBR_BASE:
                s = "## [{}] - PBR_BASE:{} 달성 - {}".format(stock_name, PBR_BASE, float(temp_data))
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

url = "https://finance.naver.com/sise/sise_market_sum.nhn"

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

stock_head = soup.find("thead").find_all("th")
data_head = [head.get_text() for head in stock_head]
data_head.pop()

stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
stockTop50_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})
result_str = ""

data_header = ['회사명']
idx = 1

Total_Message = []


for stock in stockTop50_corp:
    corp_Message = []
    stock_name = stock.get_text()
    stock_link = "https://finance.naver.com/"+stock["href"]
    flag = 1

    sub_res = requests.get(stock_link)
    sub_soup = BeautifulSoup(sub_res.text, 'lxml')

    sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"}).\
        find("thead").find_all("th", attrs={"scope":"col"})

    img_link_list = ['month3', 'year', 'year3']
    img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

    # print(stock_name)

    if idx==1:
        result_str = sub_soup.find("th", attrs={"class": "h_th2 th_cop_anal5 b_line"}).get_text()
        data_header.append(result_str)

        for value in sub_thead:
            str = value.get_text().strip()
            if (str.startswith("20")):
                result_str += str
                data_header.append(str)

        idx += 1
        # print(data_header)

    # ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
    ParamList = ['ROE(지배주주)', 'PER(배)', 'PBR(배)']

    for idx, pText in enumerate(ParamList):

        param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
        # print (param)
        result_message = getDataOfParam(idx, stock_name, param)
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

        # Total_Message.extend(result_message)
        # print (len(result_message))
        # print(result_message)

    # img_link_list = ['month3', 'year', 'year3']
    # img_link = sub_soup.find("img", attrs={"id": "img_chart_area"})['src']

    if flag == 0:

        continue

    Total_Message.extend(corp_Message)
    img1 = img_link.replace("day", img_link_list[0])
    img2 = img_link.replace("day", img_link_list[1])
    img3 = img_link.replace("day", img_link_list[2])
    Total_Message.append(img1)
    Total_Message.append(img2)
    Total_Message.append(img3)

    # writer.writerow(stock_name)
    # writer.writerow(result_str)
    # print(stock_name)
    # print(result_str)


print("\n".join(Total_Message))
