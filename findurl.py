import os
import requests


def refindURL():
    print("Do you want to start over y/n", end=" ")
    x = input()
    if x == "y" or x == "Y":
        os.system("clear")
        return findURL()

    elif x == "n" or x == "N":
        print("k. bye!")
        return False

    else:
        print("That`s not a valide answer!")
        return refindURL()


def findURL():
    print("Welcome to IsItDown.py")
    print("Please wirte a URL or URLs you want to check. (seperated by comma)")

    URLs = input().split(",")

    for URL in URLs:
        URL = URL.strip()
        if "http://" not in URL and "." not in URL:
            print(f"{URL} is not valid URL")
            rst = refindURL()
            if rst == False:
                return ""
        if "http://" not in URL and "." in URL:
            URL = "http://"+URL
        try:
            r = requests.get(URL)
            if r.status_code == requests.codes.ok:
                print(f"{URL} is up!")
        except:
            print(f"{URL} is down!")
    refindURL()


findURL()
