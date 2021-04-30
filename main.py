from core.transaction import Investment
from flask import Flask, render_template
from core.sources import BRDSource
import json

app = Flask(__name__)
app.config["DEBUG"] = True

with open("brd_founds.json", 'r') as file:
    brd_funds = json.load(file)


@app.route('/')
def found_lists():
    return render_template('test.html', funds=brd_funds.keys())


@app.route('/founds/<fund>')
def fund_data(fund):
    source = BRDSource(fund, brd_funds[fund])

    return render_template('vuans.html', fund=fund, data=source.get_data())


@app.route("/investments/<fund>")
def investment_data(fund):
    investment = Investment(fund=fund)
    source = BRDSource(fund, brd_funds[fund])
    source.get_data()
    last_value = source.data[0].value
    increase = investment.units * last_value - investment.invested_amount
    return render_template('investment.html', fund=fund, investment=investment, last_value=last_value, source=source, increase=increase)
