/*
CS 340 Project: Spring 2022
Group 2: Jenna Bucien & Herakles Li
Penguin Library System
*/

/*This temporarily disables referential constraints 
when needing to re-create or reload many tables */
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS BookCopies;
DROP TABLE IF EXISTS Patrons;
DROP TABLE IF EXISTS Checkouts;
DROP TABLE IF EXISTS CheckedBooks;
DROP TABLE IF EXISTS Locations;

/*
---TABLES---
*/
/*
Books
*/


/*
Authors 
*/
CREATE TABLE Authors(
author_id INT UNIQUE NOT NULL AUTO_INCREMENT,
author_first VARCHAR(255) NOT NULL,
author_last VARCHAR(255) NOT NULL,
PRIMARY KEY (author_id)
);


/*
BookCopies 
*/


/*
Patrons 
*/
CREATE TABLE Patrons(
patron_id INT UNIQUE NOT NULL AUTO_INCREMENT,
patron_first VARCHAR(255) NOT NULL,
patron_last VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
PRIMARY KEY (author_id)
);

/*
Checkouts
*/


/*
CheckedBooks 
*/
CREATE TABLE CheckedBooks(
checked_book_id INT UNIQUE NOT NULL AUTO_INCREMENT,
checkout_id INT UNIQUE NOT NULL,
copy_id UNIQUE NOT NULL,
returned TINYINT(),
PRIMARY KEY (checked_book_id),
FOREIGN KEY (checkout_id) REFERENCES Checkouts(checkout_id) ON DELETE SET NULL ON UPDATE CASCADE,
FOREIGN KEY (copy_id) REFERENCES BookCopies(copy_id) ON DELETE SET NULL ON UPDATE CASCADE
);


/*
Publishers 
*/
CREATE TABLE Publishers(
publisher_id INT UNIQUE NOT NULL AUTO_INCREMENT,
publisher_name VARCHAR(255) NOT NULL,
PRIMARY KEY (publisher_id)
);

/*
Locations
*/

/*
---DATA---
*/

/*
Books
*/


/*
Authors 
*/
INSERT INTO Authors(author_first, author_last)
VALUES
('Stephen', 'King'),
('Mark', 'Twain'),
('Agatha', 'Christie'),
('Jane', 'Austen'),
('Ernest', 'Hemingway');
/*
BookCopies 
*/


/*
Patrons 
*/
INSERT INTO Patrons(patron_first, patron_last, email)
VALUES
('Koko', 'Irish', 'kokoiri@egl.com'),
('Corbett', 'Farner', 'corbetfarn@gmail.com'),
('Eloise', 'Westfall', 'elwestfa@hotmail.com'),
('Zelenka', 'Fichter', 'ze.fichte@aol.com'),
('Blanche', 'Estell', 'blestell@yahoo.com');

/*
Checkouts
*/


/*
CheckedBooks 
*/
INSERT INTO CheckedBooks(checkout_id, copy_id, returned)
VALUES
(1, 12, 1),
(1, 1, 1), 
(1, 9, 1),
(2, 15, 1),
(3, 6, 1),
(3, 5, 1),
(4, 7, 1),
(5, 4, 1),
(5, 3, 1),
(5, 12, 1);

/*
Publishers 
*/
INSERT INTO Publishers(publisher_name)
VALUES
('Scribner'),
('Gallery Books'),
('SeeWolf Press'),
('Dover Publications'),
('William Morrow'),
('Penguin Books'),
('Forgotten Books');

/*
Locations
*/



SET FOREIGN_KEY_CHECKS=1;