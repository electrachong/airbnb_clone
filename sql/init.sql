/*  create 2 users with different password:
airbnb_user_dev who can access to MySQL from anywhere
airbnb_user_prod who can access to MySQL from only localhost */
CREATE USER 'airbnb_user_dev'@'127.0.0.1' IDENTIFIED BY 'ricolaisyummy21';
CREATE USER 'airbnb_user_dev'@'%' IDENTIFIED BY 'ricolaisyummy21'; 
CREATE USER 'airbnb_user_prod'@'127.0.0.1' IDENTIFIED BY 'ricolaisyummy21';

/* show the users that were created: */
\! echo "\nList of all users:"
SELECT User,Host FROM mysql.user; 

/* create 2 databases in UTF8 (utf8_general_ci):
airbnb_dev
airbnb_prod */
CREATE DATABASE airbnb_dev CHARACTER SET utf8 COLLATE utf8_general_ci; 
CREATE DATABASE airbnb_prod CHARACTER SET utf8 COLLATE utf8_general_ci;
  
/* show databases on server */
\! echo "\nList of databases on servers:"
SHOW DATABASES;

/* grant permission of:
airbnb_user_dev has all privileges to only airbnb_dev (from anywhere)
airbnb_user_prod has all privileges to only airbnb_prod */
GRANT ALL PRIVILEGES ON airbnb_dev.* TO 'airbnb_user_dev'@'127.0.0.1' IDENTIFIED BY 'ricolaisyummy21' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON airbnb_dev.* TO 'airbnb_user_dev'@'%' IDENTIFIED BY 'ricolaisyummy21' WITH GRANT OPTION; 
GRANT ALL PRIVILEGES ON airbnb_post.* TO 'airbnb_user_prod'@'127.0.0.1' IDENTIFIED BY 'ricolaisyummy21';

/* show updated privileges */
\! echo "\nUpdated privileges"
SELECT * FROM information_schema.user_privileges;


/* remember to:
Last task: create an environment variable AIRBNB_ENV with value development in your computer and production in your server */
