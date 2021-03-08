import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")
db = []


@app.route("/")
def home():
    return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
    args = request.args.to_dict()
    dicts = []
    for arg in args:
        url = f"https://www.reddit.com/r/{arg}/top/?t=month"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        d_votes = soup.find_all(
            "div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo"})
        votes = []
        d_args = []
        del d_votes[1]
        for vote in d_votes[:7]:
            vote = vote.text
            if "k" in vote:
                vote = vote.strip("k")
                vote = float(vote)*1000
            votes.append(int(vote))
            d_args.append(f"r/{arg}")
        h_titles = soup.find_all("h3", {"class": "_eYtD2XCVieq6emjKBH3m"})
        del h_titles[1]
        titles = []
        for title in h_titles[:7]:
            title = title.text
            titles.append(title)
        a_urls = soup.find_all(
            "a", {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
        urls = []
        for a_url in a_urls[:6]:
            urls.append(a_url["href"])
        for i in range(len(votes)):
            info = {"vote": votes[i], "title": titles[i],
                    "arg": d_args[i], "url": urls[i]}
            dicts.append(info)
    dicts = sorted(dicts, key=lambda x: x["vote"], reverse=True)
    return render_template("read.html", subreddits=subreddits, args=args, dicts=dicts)


app.run(host="0.0.0.0")
