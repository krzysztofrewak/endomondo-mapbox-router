FROM python:3.7 AS build
WORKDIR /application
COPY builder.py env.json ./
COPY resources ./resources
COPY assets ./assets
RUN mkdir -p ./public/data

RUN python builder.py

FROM python:3.7 AS runtime
WORKDIR /application/public
COPY --from=build /application/public ./

CMD python -m http.server

