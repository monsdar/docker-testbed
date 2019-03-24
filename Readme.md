# What is this?
This is a self-contained testbed containing
* Gitlab CE
* Gitlab CI Runner
* Two Conan Server (one for prerelease, one for release)
* A way to populate Gitlab automatically with projects

I'm using this to check out different CI concepts involving the above-mentioned tools.

# Howto?
## Start the environment
1. Extend your `/etc/hosts` with `127.0.0.1 gitlab`
1. Start via the docker-compose file: `docker-compose up --build`
1. After everything has been started (can take ~5 min) you can reach Gitlab at [http://gitlab](http://gitlab)
1. Username: `root`, Password: `qwer1234`
1. You need to trigger the gitlab-runner registration: `docker exec gitlab-runner gitlab-runner register`

## Populate the server with sample data
1. Install python dependencies: `pip install python-gitlab requests beautifulsoup4 html5lib`
1. Run `populate.py` to fill the instance with data

## Pause and resume
1. Stop execution with STRG+C
1. Start where you left off with `docker-compose up`

## Clean up
1. Run `docker-compose down -v`
