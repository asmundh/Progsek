# Simple python web application

Python webpy application running on uswgi server with nginx using docker connected to another docker-runned mysql database.

Web Server image: https://github.com/tiangolo/uwsgi-nginx-docker
webpy framework: http://webpy.org/


### prerequisites:
docker https://www.docker.com/

### Build & Run
$ docker-compose up --build

### Prune/Recreate
If you need a fresh rebuild in case of startup issues use this command (WARNING this will remove all your docker images)
$ docker system prune -a
$ docker-compose up --build

### Deploy locally

Install:
mysql
src/app/requirements.txt

Run:
Launch mysql at port 3306
Execute mysql queries
"CREATE database db;"
"USE db;"
Populate mysql by posting mysql/sql/init.sql into mysql
Edit src/app/models/database.py to point at local server
python3 src/app/main.py
