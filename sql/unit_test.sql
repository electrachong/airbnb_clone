CREATE USER 'airbnb_user_test'@'%' IDENTIFIED BY 'password';
CREATE USER 'airbnb_user_test'@'127.0.0.1' IDENTIFIED BY 'password';

CREATE DATABASE airbnb_test
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

GRANT ALL PRIVILEGES ON airbnb_test.*
    TO 'airbnb_user_test'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON airbnb_test.*
    TO 'airbnb_user_test'@'127.0.0.1' IDENTIFIED BY 'password';

FLUSH PRIVILEGES;