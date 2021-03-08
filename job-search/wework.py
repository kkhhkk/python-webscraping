import requests
from bs4 import BeautifulSoup


def extract_wework_jobs(word):
    URL = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    section = soup.find("section", {"class": "jobs"})
    results = section.find_all("li")
    for result in results[:-1]:
        title = result.find("span", {"class": "title"}).string
        company = result.find("span", {"class": "company"}).string
        re_url = result.find("a", recursive=False)["href"]
        url = f"https://weworkremotely.com{re_url}"
        jobs.append({"title": title, "company": company, "url": url})
    return jobs
