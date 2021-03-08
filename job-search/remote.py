import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}


def extract_remote_jobs(word):
    URL = f"https://remoteok.io/remote-dev+{word}-jobs"
    jobs = []
    result = requests.get(URL, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("tr", {"class": "job"})
    for result in results:
        title = result.find("h2", {"itemprop": "title"}).get_text()
        company = result["data-company"]
        url = f"httxps://remoteok.io{result['data-href']}"
        jobs.append({"title": title, "company": company, "url": url})
    return jobs
