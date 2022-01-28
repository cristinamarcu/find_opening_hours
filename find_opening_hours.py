from typing import Optional
from urllib import parse
import requests
import json
import sys


def place_id_search(placeName, Apikey) -> Optional[str]:
    parsedPlaceName = parse.quote(placeName)
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={parsedPlaceName}&inputtype=textquery&fields=place_id&key={Apikey}")
    textJson_dict=json.loads(response.text)
    if len(textJson_dict['candidates']) == 0:
        return None
    return textJson_dict['candidates'][0]['place_id']

def place_id_details(place_id, Apikey):
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name%2Crating%2Cformatted_phone_number%2Copening_hours&opening_hours&key={Apikey}")
    textJsondict = json.loads(response.text)
    if 'opening_hours' not in textJsondict['result']:
        print('Could not find opening hours for this place.')
    else:
        if textJsondict['result']['opening_hours']['open_now']:
            print('Open now', '\n')
        else:
            print('Closed', '\n')

        if 'weekday_text' in textJsondict['result']['opening_hours']:
            print('Opening hours:')
            for weekday in textJsondict['result']['opening_hours']['weekday_text']:
                  print(weekday)


'''
This program finds the place_id for 'place name' and returns the opening hours for it.
Example usage:
find_opening_hours.py 'place name' Apikey

Uses google maps places api: https://developers.google.com/maps/documentation/places/web-service/overview
'''

placename = sys.argv[1]
apikey = sys.argv[2]

place_id = place_id_search(placename, apikey)
print(placename, '\n')
if place_id != None:
    place_id_details(place_id, apikey)
else:
    print('Could not find place with that name.')
