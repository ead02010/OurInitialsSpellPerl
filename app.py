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

from datetime import datetime

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
        'venue.city': location,
        'datetime_local.gte': '2013-04-14',
        'lowest_price.gte': budget_menu
    }
    query_string = urllib.urlencode(data)
    api_url = SEATGEEK_SEARCH_URL + "?" + query_string

    response = requests.get(api_url)
    json_response = json.loads(response.text)

    start = "http://maps.googleapis.com/maps/api/staticmap";
    i = 0
    urls = {}
    for event in json_response['events']:
        lat = str(event['venue']['location']['lat'])
        lon = str(event['venue']['location']['lon'])
        coords = lat + "," + lon
        data = {
            'center': coords,
            'markers': coords,
            'zoom': '14',
            'size': '200x200',
            'sensor': 'false'
        }
        qstring = urllib.urlencode(data)
        url = start + '?' + qstring
        event['newurl']=url
        i=i+1

    return render_template('results.html',
                            location = location,
                            low_price = budget_menu,
                            events=json_response['events'])


@app.route('/save', methods=["POST"])
def save():
    return str(request.form)

if __name__ == '__main__':
    app.run(debug=True)
