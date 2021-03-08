import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python&r=true"


def extract_stackover_pages(word):
    URL = f"http://stackoverflow.com/jobs?r=true&q={word}"
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "s-pagination"})

    pages = pagination.find_all("a")

    page_numbers = []
    for page in pages[:-1]:
        page = page.get_text().strip()
        page_numbers.append(int(page))

    last_page = page_numbers[-1]
    return last_page


def extract_stackover_jobs(last_page):
    jobs = []
    for i in range(last_page):
        result = requests.get(f"{URL}&pg={i+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "grid--cell fl1"})
        for result in results:
            try:
                title = result.find(
                    "h2", {"class": "mb4 fc-black-800 fs-body3"}).find("a")["title"]
                company = result.find(
                    "h3", {"class": "fc-black-700 fs-body1 mb4"}).find_all("span")[0].string.strip()
                re_url = result.find(
                    "h2", {"class": "mb4 fc-black-800 fs-body3"}).find("a")["href"]
                url = f"https://stackoverflow.com{re_url}"
            except:
                pass
            jobs.append({"title": title, "company": company, "url": url})
    return jobs
