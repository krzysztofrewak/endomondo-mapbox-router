import glob
import json
import math
import os
import random
import sys
import xml.dom.minidom


MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
MAPBOX_STYLE_URL = os.environ["MAPBOX_STYLE_URL"]
MAP_DEFAULT_CENTER_LATITUDE = float(os.environ["MAP_DEFAULT_CENTER_LATITUDE"])
MAP_DEFAULT_CENTER_LONGITUDE = float(os.environ["MAP_DEFAULT_CENTER_LONGITUDE"])
MAP_DEFAULT_ZOOM_LEVEL = int(os.environ["MAP_DEFAULT_ZOOM_LEVEL"])
START_POINTS_RADIUS_LIMIT = float(os.environ["START_POINTS_RADIUS_LIMIT"])
ACTIVITY = os.environ["ACTIVITY"]


cache = glob.glob("./public/data/*.json")
for file in cache:
	os.remove(file)

bounded = START_POINTS_RADIUS_LIMIT > 0
if bounded:
	lng = MAP_DEFAULT_CENTER_LATITUDE
	lat = MAP_DEFAULT_CENTER_LONGITUDE
	radius = START_POINTS_RADIUS_LIMIT * 1000

	north = lat + (180/math.pi) * (radius/6378137)
	south = lat - (180/math.pi) * (radius/6378137)
	east = lng + (180/math.pi) * (radius/6378137) / math.cos(lat)
	west = lng - (180/math.pi) * (radius/6378137) / math.cos(lat)

i = 1
generated_files = []
files = glob.glob("./resources/*.tcx")
print(str(len(files)) + " files discovered.")

for file in files:
	content = xml.dom.minidom.parse(file)
	activities = content.getElementsByTagName("Activity")

	for activity in activities:
		if ACTIVITY and activity.getAttribute("Sport") != ACTIVITY:
			continue

		positions = activity.getElementsByTagName("Position")
		if not positions:
			continue

		longitude = float(positions[0].getElementsByTagName("LongitudeDegrees")[0].firstChild.nodeValue)
		latitude = float(positions[0].getElementsByTagName("LatitudeDegrees")[0].firstChild.nodeValue)

		if bounded:
			if not (longitude > west and longitude < east):
				continue

			if not (latitude > south and latitude < north):
				continue

		index = "{:03d}".format(i) + "-" + "{:09d}".format(random.randint(1, 999999))
		result = open("./public/data/{}.json".format(index), "w")
		result.write("{\"type\":\"Feature\",\"properties\":{},\"geometry\":{\"type\":\"LineString\",\"coordinates\":[")

		for position in positions:
			lng = position.getElementsByTagName("LongitudeDegrees")[0].firstChild.nodeValue
			lat = position.getElementsByTagName("LatitudeDegrees")[0].firstChild.nodeValue
			result.write("[{},{}],".format(lng, lat))

		result.seek(result.tell() - 1, os.SEEK_SET)
		result.write("]}}")
		result.close()

		generated_files.append(index)
		i += 1

index_filename = "_index-" + "{:09d}".format(random.randint(1, 999999)) + ".json"

summary = open("./public/data/" + index_filename, "w")
summary.write(json.dumps(generated_files))
summary.close()
print(str(len(generated_files)) + " files computed.")

index = open("./public/index.html", "w")
with open("assets/index.html") as template:
	template = template.read()
	template = template.replace("$INDEX_FILENAME", index_filename)
	template = template.replace("$MAPBOX_API_KEY", MAPBOX_API_KEY)
	template = template.replace("$MAPBOX_STYLE_URL", MAPBOX_STYLE_URL)
	template = template.replace("$MAP_DEFAULT_CENTER[0]", str(MAP_DEFAULT_CENTER_LATITUDE))
	template = template.replace("$MAP_DEFAULT_CENTER[1]", str(MAP_DEFAULT_CENTER_LONGITUDE))
	template = template.replace("$MAP_DEFAULT_ZOOM_LEVEL", str(MAP_DEFAULT_ZOOM_LEVEL))

	index.write(template)

print("Index file generated.")
