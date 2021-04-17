To use:

1. Build docker image:

`docker build -t coinbase-feeder .`

2. Run dependencies

2.1 by using individual docker run commands

`docker run --rm -p 6379:6379 --name redis redis`

2.2 by using docker compose

`docker-compose up`

3. Run a docker container

`docker run --rm --name coinbase-feeder coinbase-feeder`