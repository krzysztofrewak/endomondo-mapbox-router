FROM python:3.7 AS build
WORKDIR /application
COPY builder.py ./
COPY resources ./resources
COPY assets ./assets
RUN mkdir -p ./public/data

# As there is no easy way of passing environment variables in the build section of docker-compose file
# we are using arguments to do so. Those configuration parameters should be someday passed to the
# 'runtime' stage by environment variables only.

ARG MAPBOX_API_KEY
ARG MAPBOX_STYLE_URL
ARG MAP_DEFAULT_CENTER_LATITUDE
ARG MAP_DEFAULT_CENTER_LONGITUDE
ARG MAP_DEFAULT_ZOOM_LEVEL
ARG START_POINTS_RADIUS_LIMIT
ARG ACTIVITY
ARG FILENAME_FILTER

ENV MAPBOX_API_KEY=$MAPBOX_API_KEY
ENV MAPBOX_STYLE_URL=$MAPBOX_STYLE_URL
ENV MAP_DEFAULT_CENTER_LATITUDE=$MAP_DEFAULT_CENTER_LATITUDE
ENV MAP_DEFAULT_CENTER_LONGITUDE=$MAP_DEFAULT_CENTER_LONGITUDE
ENV MAP_DEFAULT_ZOOM_LEVEL=$MAP_DEFAULT_ZOOM_LEVEL
ENV START_POINTS_RADIUS_LIMIT=$START_POINTS_RADIUS_LIMIT
ENV ACTIVITY=$ACTIVITY
ENV FILENAME_FILTER=$FILENAME_FILTER

RUN python builder.py

FROM nginx:stable AS runtime
COPY --from=build /application/public /usr/share/nginx/html

