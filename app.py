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
from oauth import sign_url

app = Flask(__name__)

YELP_SEARCH_URL = 'http://api.yelp.com/v2/search'

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
        'location': location,
        'time_menu': time_menu,
        'budget_menu': budget_menu
    }
    query_string = urllib.urlencode(data)
    api_url = YELP_SEARCH_URL + "?" + query_string
    signed_url = sign_url(api_url)
    response = requests.get(signed_url)
    json_response = json.loads(response.text)

    return render_template('results.html',
                            time_menu=time_menu,
                            location=location,
                            budget_menu=budget_menu,
                            businesses=json_response['businesses'])


@app.route('/save', methods=["POST"])
def save():
    return str(request.form)

if __name__ == '__main__':
    app.run(debug=True)