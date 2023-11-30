## Python/Flask with Nginx proxy and MySQL database and React/Next.js


### Project structure:
```
.
├── compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── nginx
    └── nginx.conf

```


## Deploy with docker compose

```bash
$ docker compose up -d
$ docker compose run --rm nginx-flask-mysql-backend-1 flask database setup
```


Stop and remove the containers
```bash
$ docker compose down
```


Reset Database

```bash
docker compose run --rm nginx-flask-mysql-backend-1 flask database reset
```

seed

```bash
docker compose run --rm nginx-flask-mysql-backend-1 flask database seed
```