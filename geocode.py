#!/usr/bin/python

import argparse
import csv, subprocess
import time
import urllib
import json

parser = argparse.ArgumentParser()
parser.add_argument('-key', required=True, dest="API_KEY", default="", help="Mapzen API key")

args = parser.parse_args()
API_KEY = args.API_KEY

response = open('museums.csv', 'rb')
reader = csv.DictReader(response)

fieldnames = reader.fieldnames
fieldnames.append('Full Address')
fieldnames.append('Latitude')
fieldnames.append('Longitude')
geocoded = open('museums-geocoded.csv', 'wb')
writer = csv.DictWriter(geocoded, fieldnames=fieldnames)
writer.writeheader()

mapzen_base = "https://search.mapzen.com/v1/search?api_key=%s&text=" % API_KEY

for row in reader:
  street, city, state, zipcode = row['Street Address'], row['City'], row['State'], row['Zip Code']

  full_address = ", ".join([street, city, state, zipcode])

  geocode_url = mapzen_base + full_address # string.replace(full_address, " ", "%20")

  json_file = urllib.urlopen(geocode_url)

  json_string = json_file.read()

  json_result = json.loads(json_string)

  try:
    coordinates = json_result['features'][0]['geometry']['coordinates']
    lat = coordinates[1]
    lon = coordinates[0]

    row['Full Address'] = full_address
    row['Latitude'] = lat
    row['Longitude'] = lon

    writer.writerow(row)

    print("Processed %s" % (full_address))

    time.sleep(1)

  except KeyError, e:
    print("Failed %s" % (full_address))
