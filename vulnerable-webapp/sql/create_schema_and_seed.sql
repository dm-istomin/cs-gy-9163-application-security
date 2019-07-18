CREATE DATABASE IF NOT EXISTS vulnerable_webapp;

USE vulnerable_webapp;

CREATE TABLE IF NOT EXISTS users(
  id int auto_increment,
  username varchar(255) UNIQUE NOT NULL,
  role varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users(username, role, password) VALUES (
  'admin_user',
  'admin',
  'password'
);
INSERT INTO users(username, role, password) VALUES (
  'user1',
  'user',
  'password'
);
INSERT INTO users(username, role, password) VALUES (
  'user2',
  'user',
  'password'
);
INSERT INTO users(username, role, password) VALUES (
  'user3',
  'user',
  'password'
);
