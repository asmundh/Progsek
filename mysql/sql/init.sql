
CREATE TABLE `db`.`users` (
  `userid` INT NOT NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  PRIMARY KEY (`userid`));

insert into users values (0, "admin", "password");
insert into users values (1, "bernt", "inge");

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';
