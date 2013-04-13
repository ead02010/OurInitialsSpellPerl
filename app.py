from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for
)
import urllib
import requests
import json
import datetime

app = Flask(__name__)


SEATGEEK_SEARCH_URL = 'http://api.seatgeek.com/2/events'

@app.route('/')
def index():
    # print request.args['data2']
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    location = request.form['location']
    time_menu = request.form['time_menu']
    budget_menu = request.form['budget_menu']

    data = {
        'q': location,
        'datetime_local.gte': '2013-04-12',
        'lowest_price.gte': budget_menu
    }
    query_string = urllib.urlencode(data)
    api_url = SEATGEEK_SEARCH_URL + "?" + query_string

    response = requests.get(api_url)
    json_response = json.loads(response.text)

    return render_template('results.html',
                            location = 'location',
                            low_price = 'budget_menu',
                            events=json_response['events'])


@app.route('/save', methods=["POST"])
def save():
    return str(request.form)

if __name__ == '__main__':
    app.run(debug=True)
