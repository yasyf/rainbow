import urllib.parse, requests, os
from rainbow.helpers.mongo import geocache

def cache_geolocation_info_for_event(event, lat, lng):
    lat, lng, name = None, None, None
    cached = geocache.find_one({'original_name': event.title})

    if cached:
        lat, lng, name = cached['lat'], cached['lng'], cached['location']
    else:
        api_root = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        url_template = api_root + "?query={q}&key={k}&location={l}&radius={r}"

        api_key = os.getenv('GOOGLE_API_KEY')
        query = urllib.parse.quote_plus(event.title)
        lat_lng = '{},{}'.format(lat, lng)
        url = url_template.format(q=query, k=api_key, r=50000, l=lat_lng)
        locations = requests.get(url).json()['results']

        if locations:
            name = locations[0]['name']
            location = locations[0]['geometry']['location']
            lat, lng = location['lat'], location['lng']

    if lat:
        event.location = name
        update = {'lat': lat, 'lng': lng, 'original_name': event.title, 'location': name}
        geocache.update({'location': name}, update, upsert=True)
