from flask import Flask
from flask import request
import xml.etree.ElementTree as ET
import requests
import json


def getnews(ticker):
    r = requests.get("https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US" %ticker)
    root = ET.fromstring(r.content)
    result = []
    for elem in root.findall('.//channel/item/link'):
       result.append(elem.text.split("*")[1])
    return result


app = Flask(__name__)

@app.route('/status')
def status():
    return 'RUNNING'

@app.route('/news')
def news():
    ticker = request.values.get("ticker")
    response = app.response_class(
        response=json.dumps(getnews(ticker)),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')