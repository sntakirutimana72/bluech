CREATE DATABASE IF NOT EXISTS bluech_development;
CREATE DATABASE IF NOT EXISTS bluech_test;
CREATE DATABASE IF NOT EXISTS bluech_production;

\c bluech_development;

CREATE TABLE users (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR NOT NULL,
  display_name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE privileges (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE user_privileges (
  assignee INT NOT NULL,
  user_id INT NOT NULL,
  privilege_id INT NOT NULL,
  
  PRIMARY KEY(user_id, privilege_id),
  FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCASE,
  FOREIGN KEY(privilege_id) REFERENCES privileges (id) ON DELETE CASCADE
);

CREATE TABLE actions (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE resources (
  id INT GENERATED ALWAYS AS IDENTITY,
  res_path VARCHAR NOT NULL,
  message_id INT,
  user_id INT,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id) REFERENCES (users),
  FOREIGN KEY(message_id) REFERENCES (messages)
);

CREATE TABLE messages (
  id INT GENERATED ALWAYS AS IDENTITY,
  sender_id INT NOT NULL,
  recipient_id INT NOT NULL,
  description VARCHAR NOT NULL,
  status BOOLEAN NOT NULL DEFAULT FALSE,
  reply_to INT,
  is_edited BOOLEAN NOT NULL DEFAULT FALSE,
  
  PRIMARY KEY(id),
  FOREIGN KEY(sender_id) REFERENCES (users),
  FOREIGN KEY(recipient_id) REFERENCES (users)
);

CREATE TABLE groups (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR NOT NULL UNIQUE,
  created_by INT NOT NULL,
  is_private BOOLEAN NOT NULL,
  
  PRIMARY KEY(id),
  FOREIGN KEY(created_by) REFERENCES(users)
);

CREATE TABLE joints (
  user_id INT NOT NULL,
  group_id INT NOT NULL,
  is_group_admin BOOLEAN NOT NULL,
  
  PRIMARY KEY(user_id, group_id),
  FOREIGN KEY(user_id) REFERENCES (users),
  FOREIGN KEY(group_id) REFERENCES (groups)
);

CREATE TABLE sys_logs (
  id INT GENERATED ALWAYS AS IDENTITY,
  action_id INT NOT NULL,
  done_by INT NOT NULL,
  reference_to INT,
  summary VARCHAR,
  
  PRIMARY KEY(id),
  FOREIGN KEY(action_id) REFERENCES (actions),
  FOREIGN KEY(done_by) REFERENCES (users),
  FOREIGN KEY(reference_to) REFERENCES (users)
);
