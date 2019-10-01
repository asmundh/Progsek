
create database db;

use db

CREATE TABLE `db`.`users` (
  `userid` INT NOT NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  PRIMARY KEY (`userid`));

insert into users values (0, "admin", "password");
insert into users values (0, "bernt", "inge");


GRANT ALL PRIVILEGES ON db.* TO 'root'@'%';
