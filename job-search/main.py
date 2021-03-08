from stackover import extract_stackover_jobs, extract_stackover_pages
from wework import extract_wework_jobs
from remote import extract_remote_jobs
from flask import Flask, render_template, request, send_file, redirect
from export import export_jobs

db = {}
app = Flask("findJob")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def change_word():
    word = request.args.get("word").lower()
    if word not in db:
        last_page = extract_stackover_pages(word)
        stack_result = extract_stackover_jobs(last_page)
        wework_result = extract_wework_jobs(word)
        remote_result = extract_remote_jobs(word)
        results = stack_result + wework_result + remote_result
        db[word] = results
        return render_template("search.html", word=word, results=results)
    results = db[word]
    return render_template("search.html", word=word, results=results)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        print(word)
        if not word:
            raise Exception()
        results = db.get(word)
        if not results:
            raise Exception()
        export_jobs(word, results)
        return send_file(f"{word}_job.csv", attachment_filename=f"{word}_job.csv", as_attachment=True, cache_timeout=0)
    except:
        return redirect("/")


app.run(host="0.0.0.0")
