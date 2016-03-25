CREATE TABLE users (user_id INTEGER PRIMARY KEY ASC, username, email, password);
CREATE TABLE accounts (account_id INTEGER PRIMARY KEY ASC, account_number TEXT);
CREATE TABLE account_permissions (account_id INTEGER, user_id INTEGER, permission_id INTEGER, PRIMARY KEY (account_id, user_id, permission_id));
CREATE TABLE permissions (permission_id INTEGER PRIMARY KEY ASC, name TEXT);
CREATE TABLE transaction_types (transaction_type_id INTEGER PRIMARY KEY ASC, name TEXT);
CREATE TABLE account_transactions (transaction_id INTEGER PRIMARY KEY ASC, account_id INTEGER, amount INTEGER, transaction_type_id INTEGER, timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

