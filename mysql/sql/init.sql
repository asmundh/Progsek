
CREATE TABLE `db`.`users` (
  `userid` INT AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  PRIMARY KEY (`userid`));

insert into users values (NULL, "admin", "password");
insert into users values (NULL, "bernt", "inge");

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';
