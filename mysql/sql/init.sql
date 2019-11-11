
CREATE TABLE users (
  userid INT UNSIGNED AUTO_INCREMENT,
  username VARCHAR(45) UNIQUE NOT NULL,
  password VARCHAR(45) NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  company VARCHAR(50),
  phone_number VARCHAR(50),
  street_address VARCHAR(50),
  city VARCHAR(50),
  state VARCHAR(50),
  postal_code VARCHAR(50),
  country VARCHAR(50),
  PRIMARY KEY (userid)
);

CREATE TABLE guestbook (
  entryid INT UNSIGNED AUTO_INCREMENT, 
  text VARCHAR(255) NOT NULL,
  PRIMARY KEY (entryid)
);

/*
* Project tables
*/

CREATE TABLE teams (
  teamid INT UNSIGNED AUTO_INCREMENT,
  team_name VARCHAR(200) NOT NULL,
  write_permission BOOLEAN,
  PRIMARY KEY (teamid)
);

CREATE TABLE teams_users (
  teamid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  PRIMARY KEY (teamid, userid),
  FOREIGN KEY (teamid) REFERENCES teams(teamid),
  FOREIGN KEY (userid) REFERENCES users(userid)  
);

CREATE TABLE project_category (
  categoryid INT UNSIGNED AUTO_INCREMENT,
  category_name VARCHAR(200) UNIQUE NOT NULL,
  PRIMARY KEY (categoryid)
);

CREATE TABLE users_categories (
  userid INT UNSIGNED NOT NULL,
  categoryid INT UNSIGNED NOT NULL,
  PRIMARY KEY (userid, categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid)
);

CREATE TABLE projects (
  projectid INT UNSIGNED AUTO_INCREMENT,
  categoryid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  project_description VARCHAR(500) NOT NULL,
  project_status VARCHAR(16) NOT NULL, -- This should be either open, in progress or finished
  PRIMARY KEY (projectid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE projects_users (
  projectid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  read_permission BOOLEAN,
  write_permission BOOLEAN,
  modify_permission BOOLEAN,
  PRIMARY KEY (projectid, userid),
  FOREIGN KEY (projectid)  REFERENCES projects(projectid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE tasks (
  taskid INT UNSIGNED AUTO_INCREMENT,
  projectid INT UNSIGNED NOT NULL,
  teamid INT UNSIGNED NULL,
  title VARCHAR(200) NOT NULL,
  task_description VARCHAR(500),
  budget INT NOT NULL,
  task_status VARCHAR(64) NOT NULL, -- This should be Waiting for delivery, Delivered and waiting for acceptance, Delivery has been accepted, awaiting payment, Payment for delivery is done or Declined delivery, please revise
  feedback VARCHAR(500) NULL,
  PRIMARY KEY (taskid),
  FOREIGN KEY (teamid) REFERENCES teams(teamid)
);

CREATE TABLE task_files (
  fileid INT NOT NULL AUTO_INCREMENT,
  taskid INT UNSIGNED NOT NULL,
  filename VARCHAR(45) NOT NULL,
  PRIMARY KEY (fileid),
  FOREIGN KEY (taskid) REFERENCES tasks(taskid)
);

CREATE TABLE delivery (
  deliveryid INT UNSIGNED AUTO_INCREMENT,
  taskid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  filename VARCHAR(45) NOT NULL,
  comment VARCHAR(500),
  delivery_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  responding_userid INT NOT NULL,
  responding_time DATETIME,
  delivery_status VARCHAR(16), -- Should be Accepted, Pending or Declined
  feedback VARCHAR(500),
  PRIMARY KEY (deliveryid),
  FOREIGN KEY (taskid) REFERENCES tasks(taskid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE task_offer (
  offerid INT UNSIGNED AUTO_INCREMENT,
  taskid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  price INT,
  description VARCHAR(500),
  offer_status VARCHAR(16), -- Should be Accepted, Pending or Declined
  feedback VARCHAR(500),
  PRIMARY KEY (offerid),
  FOREIGN KEY (taskid) REFERENCES tasks(taskid)
);

/*
* Initial data
*/

insert into users values (NULL, "admin", "password", "Admin Modsen", "ntnu", "12345678", "street", "trondheim", "trondheim", "1234", "norway");

insert into guestbook values (NULL, "Hello World");

insert into project_category values (NULL, "Test");

/*
Create default database user
*/

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';
