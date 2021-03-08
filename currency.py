import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
url = "https://www.iban.com/currency-codes"


def convert_money_ask(first_code, second_code):
    try:
        value = int(input())
        if value <= 0:
            print("Input a number.")
            return convert_money_ask(first_code, second_code)
        else:
            URL = f"https://transferwise.com/gb/currency-converter/{first_code}-to-{second_code}-rate?amount={value}"
            result = requests.get(URL)
            soup = BeautifulSoup(result.text, "html.parser")
            exchange_rate = soup.find("span", {"class": "text-success"}).string
            convert_value = float(value) * float(exchange_rate)
            rst = format_currency(
                convert_value, f"{second_code}", locale="ko_KR")
            print("{} {:,} is {}".format(first_code, value, rst))
    except:
        print("That wasn`t a number")
        return convert_money_ask(first_code, second_code)


def second_ask(countries, code, first_code):
    try:
        print("#: ", end="")
        num = int(input())
        if num >= len(countries) or num < 0:
            print("Choose a number from the list.")
            return second_ask(countries, code, first_code)
        else:
            second_code = code[num]
            print(f"{countries[num]}")
            print(
                f"\nHow many {first_code} do you want to convert to {second_code}?")
            return convert_money_ask(first_code, second_code)
    except:
        print("That wasn`t a number")
        return second_ask(countries, code, first_code)


def try_except(countries, code):
    try:
        print("#: ", end="")
        num = int(input())
        if num >= len(countries) or num < 0:
            print("Choose a number from the list.")
            return try_except(countries, code)
        else:
            first_code = code[num]
            print(f"{countries[num]}")
            print("\nNow choose another country.\n")
            return second_ask(countries, code, first_code)
    except:
        print("That wasn`t a numbr")
        return try_except(countries, code)


def extract_url():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find("table", {"class": "table"})
    trs = table.find_all("tr")
    countries = []
    code = []
    for tr in trs[1:]:
        if tr.findChildren()[1].text != "No universal currency":
            countries.append(tr.findChildren()[0].text)
            code.append(tr.findChildren()[2].text)
    print("Welcome to CurrencyConvert PRO 2000")
    for idx, val in enumerate(countries):
        print(f"# {idx} {val}")
    print("\nWhere are you from? Choose a country by number.\n")
    try_except(countries, code)


extract_url()
