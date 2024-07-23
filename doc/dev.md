# Development Guide

I don't expect anyone to contribute, but let's see where this goes.

## Folder Structure

The project is structured as follows:

* `ctr4ever/` - The main backend of the application. It provides the REST API and interacts with the database
    * `cli/` - Command line interface commands for the backend
    * `helpers/` - Helper functions for the backend
    * `models/` - Database models for the backend
      * `repository/` - Repository classes for the models
    * `rest/` - The REST API of the application
      * `endpoint/` - Endpoint classes for the REST API
    * `services/` - Services for the backend (such as the `PasswordManager`)
    * `tests/` - Tests for the backend
      * `integration/` - Integration tests for the backend
      * `unit/` - Unit tests for the backend (this folder then just rebuilds the structure above)
* `doc/` - Documentation of the project
* `install/` - Master data which needs to be installed in the application (like categories, tracks, characters, etc.)
* `migrations/` - Database migrations for the backend (created with Alembic)
* `testing/` - Testing utilities for frontend and backend
* `webapp/` - The frontend of the application
  * `assets/` - Static assets
  * `public/` - Public files
  * `src/` - The main source code
    * `components/` - Reusable components
    * `layout/` - Layout components
    * `services/` - Services for the frontend (like the API client for the backend)
    * `utils/` - Various utilities
    * `views/` - The views of the application (the folder contains subfolders for each view)

## Design Choices

If you've worked in web development in the late 2000s or early 2010s you probably remember websites where the frontend was
rendered on the server and the backend was responsible for everything. Times sure have changed ...

I set up this website as a modern website - a Single Page Application (SPA) with a REST API backend. The backend is written
in Python while the frontend is written in JavaScript (TypeScript) with React.

In the backend I use the `Repository` pattern to separate the database logic from the business logic. I also make
heavy use of `Dependency Injection` (with a static `Service Container`) to make the code more testable.
Many of the unit tests use extensive mocking but it's what you have to do to test the code.

In case you need a runtime for a test that is extremely difficult to mock you can write integrations tests but it's a 
better practice to have as many unit tests as possible and only very little integration tests. One example that comes
to my mind is the base `ModelRepository` which uses the ORM query builder. This is a very difficult thing to mock, which is
why it's tested in an integration test.

I know the answer to the problem statement above is: "Well, you can separate building the query from executing the query!".
Yes ... I can. But I also want to finish this website at some point.

## Libraries

The following tech stack is used across the project:

Programming Languages:
* [Python](https://www.python.org/) - The programming language for the backend
* [TypeScript](https://www.typescriptlang.org/) - The programming language for the frontend

Technologies:
* [PostgreSQL](https://www.postgresql.org/) - The database management system
* [Docker](https://www.docker.com/) - For containerization

Libraries:
* [Flask](https://flask.palletsprojects.com/en/3.0.x/) - The backend framework
  * A few extensions are used: `Flask-SQLAlchemy`, `Flask-Migrate`, `Flask-Cors`, `Flask-JWT`
  * [SQLAlchemy](https://www.sqlalchemy.org/) - The ORM for the database
  * [Alembic](https://alembic.sqlalchemy.org/en/latest/) - For database migrations
* [React](https://reactjs.org/) - The frontend framework
  * [Vite](https://vitejs.dev/) - The frontend build tool
  * [Material UI](https://mui.com/) - The frontend component library
  * A few packages are used: `axios`, `react-router`, `zustand`

## Setup

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
