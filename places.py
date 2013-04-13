import requests, json, ConfigParser

# get location coordinates from google geocoding api
loc_query = {}
loc_query['address'] = 'Claremont, CA'
loc_query['sensor'] = 'false'
loc_url = 'https://maps.googleapis.com/maps/api/geocode/json'
loc_resp = requests.get(loc_url, params=loc_query)
coord = str(loc_resp.json()['results'][0]['geometry']['location']['lat']) + ',' + str(loc_resp.json()['results'][0]['geometry']['location']['lng'])

# get nearby places from google
config = ConfigParser.RawConfigParser()
config.read('keys.cfg')
places_query = {}
places_query['key'] = config.get('Keys', 'places')
places_query['location'] = coord
places_query['sensor'] = 'false'
places_query['radius'] = 50000
places_query['minprice'] = '1'
places_query['maxprice'] = '2'
places_query['types'] = 'amusement_park|aquarium|art_gallery|bakery|bar|bowling_alley|cafe|casino|food|movie_theater|museum|night_club|park|restaurant|shopping_mall|stadium|zoo'
places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
places_resp = requests.get(places_url, params=places_query)
len(places_resp.json()['results'])

# get place details
details = {}
for x in places_resp.json()['results']:
  detail_query = {}
  detail_query['key'] = config.get('Keys', 'places')
  detail_query['reference'] = x['reference']
  detail_query['sensor'] = 'false'
  detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'
  detail_resp = requests.get(detail_url, params=detail_query)
  details[x['reference']] = detail_resp.json()['result']

# filter by open and closing time
day = 0
start = '1500'
end = '1700'
filtered = {}
for ref in details:
  if 'opening_hours' in details[ref]:
    hours = details[ref]['opening_hours']['periods'][day]
    if 'open' in hours and 'close' in hours:
      if 'time' in hours['open'] and 'time' in hours['close']:
        if (start > hours['open']['time']) & (end < hours['close']['time']):
          filtered[ref] = details[ref]

for x in filtered:
  print filtered[x]
