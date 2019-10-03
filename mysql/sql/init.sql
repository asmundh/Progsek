
CREATE TABLE `db`.`users` (
  'id' INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  );

insert into users values ("admin", "password");
insert into users values ("bernt", "inge");

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';
