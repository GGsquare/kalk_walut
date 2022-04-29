from asyncore import write
import csv
from pydoc import Doc
import requests
import os
from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
rates = response.json()
#print(rates[0]['rates'])
rates=rates[0]["rates"]
"""rates = [{"currency":"dolar amerykański","code":"USD","bid":4.2113,"ask":4.2963},
{"currency":"dolar australijski","code":"AUD","bid":3.1517,"ask":3.2153},
{"currency":"dolar kanadyjski","code":"CAD","bid":3.3474,"ask":3.4150},
{"currency":"euro","code":"EUR","bid":4.5962,"ask":4.6890},
{"currency":"forint (Węgry)","code":"HUF","bid":0.012116,"ask":0.01236},
{"currency":"frank szwajcarski","code":"CHF","bid":4.5147,"ask":4.6059},
{"currency":"funt szterling","code":"GBP","bid":5.5037,"ask":5.6149},
{"currency":"jen (Japonia)","code":"JPY","bid":0.033975,"ask":0.034661},
{"currency":"korona czeska","code":"CZK","bid":0.1872,"ask":0.1910},
{"currency":"korona duńska","code":"DKK","bid":0.6180,"ask":0.6304},
{"currency":"korona norweska","code":"NOK","bid":0.4789,"ask":0.4885},
{"currency":"korona szwedzka","code":"SEK","bid":0.4456,"ask":0.4546},
{"currency":"SDR (MFW)","code":"XDR","bid":5.7764,"ask":5.8930}]"""
rates.append({"currency":"polski złoty", "code":"PLN", "bid":1, "ask":1})
ask_dict = {}
bid_dict = {}
for i in rates:
    currency = (i["currency"])
    code = (i["code"])
    bid = (i["bid"])
    ask = (i["ask"])
    ask_dict[code]=ask
    bid_dict[code]=bid
    #print(currency, code, bid, ask)
filename = "nbp.csv"
with open(filename, 'w') as csvfile:
    header = [key for key in rates[0].keys()]
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=header)
    writer.writeheader()
    writer.writerows(rates)
@app.route('/', methods=['GET', 'POST'])
def kalkulator_walut():
    if request.method == 'POST':
        try:
            amount = request.form['amount']
            amount = float(amount)
            exchange = request.form['exchange']
            rate = ask_dict[exchange]
            rate = float(rate)
            result = amount / rate
            exchange_code = exchange
            exchange_name = exchange
            return render_template('kalkulator_walut.html', result=round(result, 2), amount=amount, 
                                                            exchange_code=exchange_code, exchange_name=exchange_name)
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
    else:
        return render_template('kalkulator_walut.html')
@app.route('/2/', methods=['GET', 'POST'])
def kalkulator_walut2():
    if request.method == 'POST':
        try:
            amount2 = request.form['amount2']
            amount2 = float(amount2)
            sell = request.form['sell']
            rate2 = bid_dict[sell]
            rate2 = float(rate2)
            result2 = rate2 * amount2
            sell_code = sell
            sell_name = sell
            return render_template('kalkulator_walut.html', result2=round(result2, 2), amount2=amount2, 
                                                            sell_code=sell_code, sell_name=sell_name)
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
    else:
        return render_template('kalkulator_walut.html')
if __name__ == "__main__":
    app.run(debug=True)