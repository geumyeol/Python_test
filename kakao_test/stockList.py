

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

def getDataOfParam(stock_name, param):

    data_body = []
    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param})
    result_str = sub_title.get_text().strip()
    data_body.append(stock_name)
    data_body.append(result_str)

    data = sub_tbody.find("td")
    str = data.get_text().strip()

    data_body.append(str)

    for value in data.find_next_siblings():
        str = value.get_text().strip()
        result_str += str
        data_body.append(str)

    # writer.writerow(result_str)
    # print(result_str)

    # print(data_header)
    print(data_body)

filename = "naver_stock_1to200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline='')
writer = csv.writer(f, delimiter='\t')

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

for stock in stockTop50_corp:
    stock_name = stock.get_text()
    stock_link = "https://finance.naver.com/"+stock["href"]

    sub_res = requests.get(stock_link)
    sub_soup = BeautifulSoup(sub_res.text, 'lxml')

    sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"}).\
        find("thead").find_all("th", attrs={"scope":"col"})


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
        print(data_header)

    ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
    for pText in ParamList:
        param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
        getDataOfParam(stock_name, param)

    break
    # writer.writerow(stock_name)
    # writer.writerow(result_str)
    # print(stock_name)
    # print(result_str)


# print(stockTop50[0].get_text())
"""
for row in stock_list:
    columns = row.find_all("td")
    if len(columns) <= 1:
        continue


    # for idx, column in enumerate(columns):
    #     ROE, PER, PBR 수치에 대한 조건
    data = [column.get_text().strip() for column in columns]
    print(data)"""