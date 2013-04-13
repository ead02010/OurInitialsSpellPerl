import requests, json, ConfigParser

# get location coordinates from google geocoding api
loc_query = {}
loc_query['address'] = 'Claremont, CA' #todo
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
places_query['radius'] = 50000  #todo, maximum meters distance
places_query['minprice'] = '1'  #todo, range 0 to 4
places_query['maxprice'] = '2'  #todo
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
day = 0  #todo, 0 is sunday
start = '1500'  #todo, military time
end = '1700'  #todo
filtered = {}
for ref in details:
  if 'opening_hours' in details[ref]:
    hours = details[ref]['opening_hours']['periods'][day]
    if 'open' in hours and 'close' in hours:
      if 'time' in hours['open'] and 'time' in hours['close']:
        if (end > hours['open']['time']) and (start < hours['close']['time']):
          filtered[ref] = details[ref]

# sort by rating
rated = {}
for ref in filtered:
  if 'rating' in filtered[ref]:
    rated[ref] = filtered[ref]
# if num entries are rated, use those
best = []
num = 3
if len(rated) >= num:
  for x in sorted(rated.items(), key=lambda e: e[1]['rating'])[-num:]:
    print x[1]['rating']
    best.append(x)
# if not, use the first num returned
else:
  for x in filtered.items()[:num]:
    print x[1]['rating']
    best.append(x)

for x in best:
  print str(x[1]['geometry']['location']['lat']) + ',' + str(x[1]['geometry']['location']['lng'])
