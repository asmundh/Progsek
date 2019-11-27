# Simple python web application

Python webpy application running on uswgi server with nginx using docker connected to another docker-runned mysql database.

Web Server image: https://github.com/tiangolo/uwsgi-nginx-docker
webpy framework: http://webpy.org/


### Prerequisites:
docker https://www.docker.com/

On linux docker is started with

$ sudo systemctl start docker

To run docker-compose without sudo the user must be added to the usergroup:

https://docs.docker.com/install/linux/linux-postinstall/

### Build & Run

$ docker-compose up --build

### Prune/Recreate
If you need a fresh rebuild in case of startup issues use this command (WARNING this will remove all your docker images)

$ docker system prune -a

$ docker-compose up --build

# Deploy locally

Prerequisites:

mysql

python3

src/app/requirements.txt

### Run Datatbase:
Launch mysql at default port (3306)

$ systemctl start mysqld

Log in to database

$ sudo mysql -u root

Insert mysql queries

"CREATE database db;"

"USE db;"

"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root');"

Then populate databse by posting mysql/sql/init.sql into 
mysql

Edit src/app/models/database.py to point at local server



###Run app

$ cd src/app/

$ python3 src/app/main.py
