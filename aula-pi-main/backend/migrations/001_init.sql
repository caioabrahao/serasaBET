CREATE TABLE IF NOT EXISTS users (
  id CHAR(36) NOT NULL, 
  email VARCHAR(128) NOT NULL, 
  password VARCHAR(128) NOT NULL, 
  name VARCHAR(128) NOT NULL,
  balance DECIMAL(19, 4) NOT NULL DEFAULT '0.0000',
  date_of_birth DATETIME NOT NULL,
  role ENUM('user', 'admin') NOT NULL DEFAULT 'user',

  PRIMARY KEY (id),
  UNIQUE INDEX unique_email (email)
);

CREATE TABLE IF NOT EXISTS events (
  id CHAR(36) NOT NULL,
  title VARCHAR(128) NOT NULL,
  description VARCHAR(128) NOT NULL,
  odds_value DECIMAL(19, 4) NOT NULL,
  event_date DATETIME NOT NULL,
  betting_start_date DATETIME NOT NULL,
  betting_end_date DATETIME NOT NULL,
  created_by CHAR(36) NOT NULL,
  status ENUM(
    'awaiting_evaluation', 
    'approved', 
    'disapproved', 
    'revoked', 
    'finished'
  ) NOT NULL DEFAULT 'awaiting_evaluation',
  disapproval_reason TEXT,

  FOREIGN KEY (created_by) REFERENCES users(id),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS bets (
  id CHAR(36) NOT NULL,
  user_id CHAR(36) NOT NULL,
  event_id CHAR(36) NOT NULL,
  bet ENUM('yes', 'no') NOT NULL,
  amount DECIMAL(19, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS transactions (
  id CHAR(36) NOT NULL,
  type ENUM('deposit', 'withdraw') NOT NULL,
  user_id CHAR(36) NOT NULL,
  amount DECIMAL(19, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
