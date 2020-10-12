

"""
1. Top 50
2. PER 30% 미만
3. PBR 5 미만
4. ROE 10 이상
5. 3개월 / 1년 / 3년
"""
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_market_sum.nhn"

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

stock_head = soup.find("thead").find_all("th")
data_head = [head.get_text() for head in stock_head]
data_head.pop()

stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")

for row in stock_list:
    columns = row.find_all("td")
    if len(columns) <= 1:
        continue

    data = [column.get_text().strip() for column in columns]
    print(data)