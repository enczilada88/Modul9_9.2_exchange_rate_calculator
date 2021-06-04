import requests
import csv

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/rates', methods=['GET', 'POST'])
def exchange():
    money_dict = get_data()
    if request.method == "GET":
        price = None
        return render_template("currency_exchange.html", money_list=money_dict.keys(), price=price)
    elif request.method == "POST":
        chosen_currency = request.form["currency"]
        amount = float(request.form["amount"])
        price = round(amount * money_dict[chosen_currency]["ask"], ndigits=2)
        return render_template("currency_exchange.html", money_list=money_dict.keys(), price=price)


def get_data():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()

    with open("currencies.csv", mode="w") as currencies:
        currency_writer = csv.writer(currencies, delimiter=";")
        currency_writer.writerow(["currency", "code", "bid", "ask"])
        for i in range(len(data[0]["rates"])):
            currency_writer.writerow([
                data[0]["rates"][i]["currency"],
                data[0]["rates"][i]["code"],
                data[0]["rates"][i]["bid"],
                data[0]["rates"][i]["ask"],
            ])
    currency_dict = {}
    for i in range(len(data[0]["rates"])):
        code = data[0]["rates"][i]["code"]
        bid = float(data[0]["rates"][i]["bid"])
        ask = float(data[0]["rates"][i]["ask"])
        currency_dict[code] = {"bid": bid, "ask": ask}

    return currency_dict

if __name__ == '__main__':
    app.run()