![Rendered example](https://i.imgur.com/aA9UgUc.png)

## Usage
Put all your workout files to `./resources` directory. You can download them one-by-one from Endomondo's dashboard or request all of them according to [this Suppport page](https://support.endomondo.com/hc/en-us/articles/360006081933-How-to-download-your-Endomondo-user-data-). Only TCX files are supported right now. You can put any other files to `./resources` directory and they will be ignored.

Next, use provided `docker-compose.yml` template to create personal configuration.
```
cp docker-compose.yml.template docker-compose.yml
```

Fill configuration fields in build arguments (you have to at least provide Mapbox API key):
* `MAPBOX_API_KEY`: your own Mapbox API key; you can generate it for free by registering on [https://www.mapbox.com/](https://www.mapbox.com/);
* `MAPBOX_STYLE_URL`: by default it's a [Mapbox Dark](https://www.mapbox.com/maps/light-dark/), but you can put whatever you like;
* `MAP_DEFAULT_CENTER`: center point for generated map;
* `MAP_DEFAULT_ZOOM_LEVEL`: zoom level for generated map in form of array of longitude and latitude;
* `START_POINTS_RADIUS_LIMIT`: you can filter all workouts that started further than chosen kilometer range; it can be helpful if you'd like to change scope of map for only one city; insert `0` to remove limits;
* `ACTIVITY`: specifies kind of activity to draw (tracks with other kind of activites fill be filtered out); leave empty to include all tracks;
* `FILENAME_FILTER`: filters TCX files names from `resources` directory; for example put `2020*.tcx` to filter files with name starting with `2020`. 

Build image:
```
docker-compose build
```

Run service:
```
docker-compose up
```

Service will be available on http://localhost:8080/ (you can tweak it in the `docker-compose.yml`).

