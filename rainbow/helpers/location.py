from xml.dom import minidom
import urllib.request, math

def get_closest_event_lat_lng(event, lat, lng):
    min_arc = 2
    closest_loc = None

    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=%s&key=AIzaSyCfWZ1V6gJ-51aVwIbXuLbh3u-rsGDxaDE" % event.title.replace(' ', '+')
    locations = minidom.parse(urllib.request.urlopen(url)).getElementsByTagName("location")
    for location in locations:
        loc_lat = float(location.getElementsByTagName("lat")[0].firstChild.nodeValue)
        loc_lng = float(location.getElementsByTagName("lng")[0].firstChild.nodeValue)
        arc = distance_on_unit_sphere(lat, lng, loc_lat, loc_lng)
        if arc < min_arc:
            min_arc = arc
            closest_loc = (loc_lat, loc_lng)

    if closest_loc == None:
        raise Exception("no locations returned from searching: " + event.title)
    else:
        return closest_loc

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    return arc
