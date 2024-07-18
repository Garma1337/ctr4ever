# ctr4ever

This is the new website of ctr4ever. It was due an overhaul, wasn't it?

## Libraries

The new website uses a Python backend built on [Flask](https://flask.palletsprojects.com/en/3.0.x/) (with a few extensions)
and uses a React (TypeScript) frontend based on [Vite](https://vitejs.dev/) and [Material UI](https://mui.com/). [PostgreSQL](https://www.postgresql.org/) 
is used as a database management system. It is recommended to run the application through [Docker](https://www.docker.com/) - at least for a production environment.

## Development

Create a virtual environment (or don't - your choice) and install the dependencies from the requirements.txt:

```bash
$ pip install -r requirements.txt
$ pip install -e .
```

Running the application is then pretty straightforward:

```bash
$ flask --app ctr4ever run
```

To spawn the PostgreSQL database with [Adminer](https://www.adminer.org/en/), you can use the `dev.docker-compose.yml` file.

```bash
$ docker-compose -f dev.docker-compose.yml up
```

This will spawn a docker compose with 2 containers: A PostgreSQL container and an Adminer container.
From there on you can start development.

### Faker

If you don't have a database dump or you want to do performance testing you might need more data than what we have as actual submitted time.
For that reason you can use the `Faker` to generate a bunch of fake submissions. This is helpful if you need to test anything
that requires a large dataset.

```bash
$ flask --app ctr4ver faker --help
```

## Deployment

The project contains a `Dockerfile` and `docker-compose.yml`. Just run the docker compose file and this will spawn
all the necessary containers and start the application. Make sure you expose file systems and other necessary things
(for example to backup the database regularly).

```bash
$ docker-compose -f docker-compose.yml up
```

After the initial deployment you need to apply migrations to get the database schema set up:

```bash
$ flask --app ctr4ever db upgrade head
```

After all migrations have been applied you need to set up the initial master data of the website
such as categories, tracks, characters and so on.

```bash
$ flask --app ctr4ever installer categories
$ flask --app ctr4ever installer characters
$ flask --app ctr4ever installer countries
$ flask --app ctr4ever installer engine_styles
$ flask --app ctr4ever installer game_versions
$ flask --app ctr4ever installer platforms
$ flask --app ctr4ever installer rulesets
$ flask --app ctr4ever installer standards
$ flask --app ctr4ever installer tracks
```
