#reset DB
DROP DATABASE IF EXISTS `inventory`;
CREATE DATABASE IF NOT EXISTS `inventory`;

use `inventory`;

#emulating a Best Buy for test values
#Create Tables

#user table
CREATE TABLE user_table (
	id int(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username  VARCHAR(30) NOT NULL,
	password  VARCHAR(30) NOT NULL,
	reg_date TIMESTAMP
);

#Add Test Values
INSERT INTO
	`user_table` (id, username, password) 
VALUES
	(1, 'Donald', 'Duck'),
	(2, 'Daisy', 'Duck');

#inventory table
CREATE TABLE inv_table (
	id int(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name  VARCHAR(30) NOT NULL,
	description VARCHAR(30),
	price DECIMAL(10, 2) NOT NULL,
	stock int(11) DEFAULT 0,
	is_public TINYINT(1) DEFAULT 0,
	reg_date TIMESTAMP
);

#Add Test Values
INSERT INTO
	`inv_table` (id, name, description, price, stock, is_public) 
VALUES
	(1, 'iphone 5', '2013 iphone', 99.99, 80, 1),
	(2, 'Samsung TV - SK8000', '65" TV with HDR', 649.99, 25, 0),
	(3, 'PS4', 'Plays video games', 299.99, 109, 1),
	(4, 'Infinity War DVD', 'Avengers movie', 19.99, 56, 1),
	(5, 'Macbook Pro', 'A 2015 Apple laptop', 799.99, 14, 1),
	(6,	'iphone Charger', 'Ultra fast charging for iphone', 9.99, 221, 1),
	(7,	'Drake album', 'Scorpion - June 2018', 14.99, 520, 1);


#orders table
CREATE TABLE orders_table (
	id int(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	product_id int(10) UNSIGNED,
	employee_id int(10) UNSIGNED,
	price int(11) DEFAULT 0.00,
	amount int(11) DEFAULT 0,
	reg_date TIMESTAMP,

   FOREIGN KEY (product_id) REFERENCES inv_table(id),
   FOREIGN KEY (employee_id) REFERENCES user_table(id)
);

#Add Test Values
INSERT INTO
	`orders_table` (id, product_id, employee_id, price, amount, reg_date) 
VALUES
	(1, 1, 2, 99.99, 1, '2018-12-09 19:22:39'),
	(2, 1, 2, 109.99, 1, '2018-10-04 14:42:39'),
	(3, 1, 1, 109.99, 1, '2018-10-04 14:21:10'),
	(4, 1, 2, 109.99, 1, '2018-10-04 9:11:55'),
	(5, 1, 1, 119.99, 1, '2018-10-04 21:53:42'),
	(6, 1, 1, 119.99, 2, '2018-10-04 13:57:32'),
	(7, 1, 1, 119.99, 3, '2018-10-04 2:59:00'),
	(8, 1, 2, 119.99, 1, '2018-10-04 4:59:00'),
	(9, 1, 1, 149.99, 2, '2018-10-04 5:42:39'),
	(10, 1, 2, 149.99, 1, '2018-10-04 18:08:34'),
	(11, 1, 1, 149.99, 1, '2018-10-04 15:45:39'),
	(12, 1, 2, 149.99, 1, '2018-10-04 11:12:32'),
	(13, 1, 2, 169.99, 1, '2018-10-04 10:42:39'),
	(14, 1, 2, 199.99, 4, '2018-10-04 9:22:39');




#new features ideas
#show statistics for each item bought, graphs etc
#output csv file of timeline of transactions of the last week / month/ year
#peak times analytics
#refund
#add memberships - tracking spending habits - export a csv file of this data - use machine learning algo
