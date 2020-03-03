![Rendered example](https://i.imgur.com/aA9UgUc.png)

# Usage
Put all your workout files to `./resources` directory. Only TCX files are supported right now. You can download them one-by-one from Endomondo's dashboard or request all of them according to [this Suppport page](https://support.endomondo.com/hc/en-us/articles/360006081933-How-to-download-your-Endomondo-user-data-).

Next, create an environment file based on provided example and fill with proper data:
```
cp env.example.json env.json
nano env.json
```

Run builder via Docker-compose to build router:
```
docker-compose run -w /application python python builder.py
```

Serve and go to `://localhost:11123`:
```
docker-compose run -p 11123:8000 -w /application/public python python -m http.server
```