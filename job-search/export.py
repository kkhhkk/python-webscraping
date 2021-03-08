import csv


def export_jobs(word, results):
    save_name = f"{word}_job.csv"
    file = open(save_name, mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for result in results:
        writer.writerow(list(result.values()))
    return
