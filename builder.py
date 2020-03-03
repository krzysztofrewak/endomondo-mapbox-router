import glob
import json
import math
import os
import sys
import xml.dom.minidom


with open("env.json") as environment:
	environment = json.load(environment)

bounded = environment["start_points_radius_limit"] > 0 
if bounded:
	lng = environment["map_default_center"][0]
	lat = environment["map_default_center"][1]
	radius = float(environment["start_points_radius_limit"]) * 1000

	north = lat + (180/math.pi) * (radius/6378137)
	south = lat - (180/math.pi) * (radius/6378137)
	east = lng + (180/math.pi) * (radius/6378137) / math.cos(lat)
	west = lng - (180/math.pi) * (radius/6378137) / math.cos(lat)

files = []
i = 1

for file in glob.glob("./resources/*.tcx"):
	content = xml.dom.minidom.parse(file)
	activities = content.getElementsByTagName("Activity")

	for activity in activities:
		if activity.getAttribute("Sport") != "Biking":
			continue

		positions = activity.getElementsByTagName("Position")
		longitude = float(positions[0].getElementsByTagName("LongitudeDegrees")[0].firstChild.nodeValue)
		latitude = float(positions[0].getElementsByTagName("LatitudeDegrees")[0].firstChild.nodeValue)

		if bounded:
			if not (longitude > west and longitude < east):
				continue

			if not (latitude > south and latitude < north):
				continue

		index = "{:03d}".format(i)
		result = open("./public/data/{}.json".format(index), "w")
		result.write("{\"type\":\"Feature\",\"properties\":{},\"geometry\":{\"type\":\"LineString\",\"coordinates\":[")

		for position in positions:
			lng = position.getElementsByTagName("LongitudeDegrees")[0].firstChild.nodeValue
			lat = position.getElementsByTagName("LatitudeDegrees")[0].firstChild.nodeValue
			result.write("[{},{}],".format(lng, lat))

		result.seek(result.tell() - 1, os.SEEK_SET)
		result.write("]}}")
		result.close()

		files.append(index)
		i += 1

summary = open("./public/data/_index.json", "w")
summary.write(json.dumps(files))
summary.close()

index = open("./public/index.html", "w")
with open("assets/index.html") as template:
	template = template.read()
	template = template.replace("$MAPBOX_API_KEY", environment["mapbox_api_key"])
	template = template.replace("$MAPBOX_STYLE_URL", environment["mapbox_style_url"])
	template = template.replace("$MAP_DEFAULT_CENTER[0]", str(environment["map_default_center"][0]))
	template = template.replace("$MAP_DEFAULT_CENTER[1]", str(environment["map_default_center"][1]))
	template = template.replace("$MAP_DEFAULT_ZOOM_LEVEL", str(environment["map_default_zoom_level"]))

	index.write(template)