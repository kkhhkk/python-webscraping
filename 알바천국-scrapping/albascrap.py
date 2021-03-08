import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"
result = requests.get(alba_url)
soup = BeautifulSoup(result.text, "html.parser")
lists = soup.find_all("li", {"class": "impact"})

for list in lists:
    url = list.find("a")["href"]
    company = list.find("span", {"class": "company"}).string

    save_name = f"{company}.csv"
    file = open(save_name, mode="w")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    i = 1
    rst = True
    while (rst):
        find_company = requests.get(f"{url}/job/brand/?page={i}")
        find_soup = BeautifulSoup(find_company.text, "html.parser")
        tbody = find_soup.find("tbody")
        tr = tbody.find_all("tr")
        if tbody.get_text() == "해당 조건/분류에 일치하는 채용정보가 없습니다.":
            rst = False
        for td in tr:
            save_info = []
            try:
                place = td.find("td", {"class": "local"}).get_text()
                title = td.find("span", {"class": "company"}).get_text()
                time = td.find("span", {"class": "time"}).get_text()
                pay = td.find("td", {"class": "pay"}).get_text()
                date = td.find("td", {"class": "regDate"}).get_text()
                save_info.append(place)
                save_info.append(title)
                save_info.append(time)
                save_info.append(pay)
                save_info.append(date)
                writer.writerow(save_info)
            except:
                print("none")
        i += 1
