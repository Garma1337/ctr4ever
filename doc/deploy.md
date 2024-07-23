# Deployment

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
$ flask --app ctr4ever installer categories --filename "install/categories.json"
$ flask --app ctr4ever installer characters --filename "install/characters.json"
$ flask --app ctr4ever installer countries --filename "install/countries.json"
$ flask --app ctr4ever installer engine_styles --filename "install/engine_styles.json"
$ flask --app ctr4ever installer game_versions --filename "install/game_versions.json"
$ flask --app ctr4ever installer platforms --filename "install/platforms.json"
$ flask --app ctr4ever installer rulesets --filename "install/rulesets.json"
$ flask --app ctr4ever installer standards --filename "install/standards.json"
$ flask --app ctr4ever installer tracks --filename "install/tracks.json"
```

The installer can also be used to update existing records. It is possible to edit existing fields
or add completely new entries. Just run the installer again and it will create new entries or update existing ones.
