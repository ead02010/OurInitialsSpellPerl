import requests, json, ConfigParser

# get location coordinates from google geocoding api
loc_query = {}
loc_query['address'] = 'Claremont, CA' #todo
loc_query['sensor'] = 'false'
loc_url = 'https://maps.googleapis.com/maps/api/geocode/json'
loc_resp = requests.get(loc_url, params=loc_query)
coord = str(loc_resp.json()['results'][0]['geometry']['location']['lat']) + ',' + str(loc_resp.json()['results'][0]['geometry']['location']['lng'])

# get price category from $ value
dollars = 75; # todo
if dollars > 55:
  price = 4
elif dollars > 35:
  price = 3
elif dollars > 20:
  price = 2
elif dollars > 10:
  price = 1
else:
  price = 0

# get nearby places from google
config = ConfigParser.RawConfigParser()
config.read('keys.cfg')
places_query = {}
places_query['key'] = config.get('Keys', 'places')
places_query['location'] = coord
places_query['sensor'] = 'false'
places_query['radius'] = 50000  #todo, maximum meters distance
places_query['minprice'] = 0
places_query['maxprice'] = price
places_query['types'] = 'amusement_park|aquarium|art_gallery|bakery|bar|bowling_alley|cafe|casino|food|movie_theater|museum|night_club|park|restaurant|shopping_mall|stadium|zoo'
places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
places_resp = requests.get(places_url, params=places_query)

# get place details
details = []
for x in places_resp.json()['results']:
  detail_query = {}
  detail_query['key'] = config.get('Keys', 'places')
  detail_query['reference'] = x['reference']
  detail_query['sensor'] = 'false'
  detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'
  detail_resp = requests.get(detail_url, params=detail_query)
  details.append(detail_resp.json()['result'])

# filter by open and closing time
day = 0  #todo, 0 is sunday
start = '1500'  #todo, military time
end = '1700'  #todo
filtered = []
for x in details:
  if 'opening_hours' in x:
    hours = x['opening_hours']['periods'][day]
    if 'open' in hours and 'close' in hours:
      if 'time' in hours['open'] and 'time' in hours['close']:
        if (end > hours['open']['time']) and (start < hours['close']['time']):
          filtered.append(x)

# sort by rating
rated = []
for x in filtered:
  if 'rating' in x:
    rated.append(x)

# if num entries are rated, use those
best = []
num = 3
if len(rated) >= num:
  for x in sorted(rated, key=lambda e: e['rating'])[-num:]:
    print x['rating']
    best.append(x)
# if not, use the first num returned
else:
  for x in filtered[:num]:
    best.append(x)

# location
for x in best:
  print str(x['geometry']['location']['lat']) + ',' + str(x['geometry']['location']['lng'])

# page url 
for x in best:
  print x['url']

# rating
for x in best:
  if 'rating' in x:
    print x['rating']


