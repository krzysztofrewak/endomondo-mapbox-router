![Rendered example](https://i.imgur.com/aA9UgUc.png)

## Usage
Put all your workout files to `./resources` directory. You can download them one-by-one from Endomondo's dashboard or request all of them according to [this Suppport page](https://support.endomondo.com/hc/en-us/articles/360006081933-How-to-download-your-Endomondo-user-data-). Only TCX files are supported right now. You can put any other files to `./resources` directory and they will be ignored.

Next, create an environment file based on provided example and fill with proper data:
```
cp env.example.json env.json
```

Put following data to the JSON keys:
* `mapbox_api_key`: your own Mapbox API key; you can generate it for free by registering on [https://www.mapbox.com/](https://www.mapbox.com/);
* `mapbox_style_url`: by default it's a [Mapbox Dark](https://www.mapbox.com/maps/light-dark/), but you can put whatever you like;
* `map_default_center`: center point for generated map;
* `map_default_zoom_level`: zoom level for generated map in form of array of longitude and latitude;
* `start_points_radius_limit`: you can filter all workouts that started further than chosen kilometer range; it can be helpful if you'd like to change scope of map for only one city; insert `0` to remove limits.

Run builder via Docker-compose to build router and static API for the map:
```
docker-compose run -w /application python python builder.py
```

Serve simple HTTP server (of course you can use your own solution for that) and go to `://localhost:11123` (or whatever other port you want):
```
docker-compose run -p 11123:8000 -w /application/public python python -m http.server
```