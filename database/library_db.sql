/*
 CS 340 Project: Spring 2022
 Group 2: Jenna Bucien & Herakles Li
 Penguin Library System
 */
/*This temporarily disables referential constraints 
 when needing to re-create or reload many tables */
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS BookCopies;
DROP TABLE IF EXISTS Patrons;
DROP TABLE IF EXISTS Checkouts;
DROP TABLE IF EXISTS CheckedBooks;
DROP TABLE IF EXISTS Locations;

/* ---TABLES---

/*
 Locations
 */
CREATE TABLE Locations (
    location_id INT UNSIGNED AUTO_INCREMENT,
    location_name VARCHAR (255) NOT NULL,
    location_address VARCHAR (255) NOT NULL,
    PRIMARY KEY (location_id)
);


/*
 Authors 
 */
CREATE TABLE Authors (
    author_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    author_first VARCHAR(255) NOT NULL,
    author_last VARCHAR (255) NOT NULL,
    PRIMARY KEY (author_id)
);

/*
 Publishers 
 */
CREATE TABLE Publishers (
    publisher_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    publisher_name VARCHAR (255) NOT NULL,
    PRIMARY KEY (publisher_id)
);

/*
 Books
 */
CREATE TABLE Books (
    book_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    isbn VARCHAR (17) NOT NULL,
    title VARCHAR (255) NOT NULL,
    author_id INT,
    year CHAR (4),
    publisher_id INT,
    PRIMARY KEY (book_id),
    FOREIGN KEY (author_id) REFERENCES Authors (author_id) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES Publishers (publisher_id) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE
);

 /*
 BookCopies 
 */
CREATE TABLE BookCopies (
    copy_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    book_id INT,
    location_id INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (copy_id),
    FOREIGN KEY (book_id) REFERENCES Books (book_id) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES Locations (location_id) 
                ON DELETE SET NULL 
                ON UPDATE CASCADE
);

/*
 Patrons 
 */
CREATE TABLE Patrons (
    patron_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    patron_first VARCHAR (255) NOT NULL,
    patron_last VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL,
    PRIMARY KEY (patron_id)
);

/*
 Checkouts
 */
CREATE TABLE Checkouts (
    checkout_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    patron_id INT,
    checkout_date DATE NOT NULL,
    return_date DATE NOT NULL,
    PRIMARY KEY (checkout_id),
    FOREIGN KEY (patron_id) REFERENCES Patrons (patron_id) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE
);

/*
 CheckedBooks 
 */
CREATE TABLE CheckedBooks (
    checked_book_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    checkout_id INT,
    copy_id INT,
    returned TINYINT (1),
    PRIMARY KEY (checked_book_id),
    FOREIGN KEY (checkout_id) REFERENCES Checkouts (checkout_id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE,
    FOREIGN KEY (copy_id) REFERENCES BookCopies(copy_id) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE
);


/* -------------DATA-------------------

/*
 Locations
 */
INSERT INTO
    Locations (location_name, location_address)
VALUES
    ('Little Penguin Library', '67 Cooper Ave'),
    ('Macaroni Penguin Library', '658 Lincoln Lane'),
    ('Emperor Penguin Library', '7580 Devon Rd'),
    ('Rockhopper Penguin Library', '319 6th St'),
    ('Royal Penguin Library', '309 East Walnutwood Lane');

/*
 Authors 
 */
INSERT INTO
    Authors (author_first, author_last)
VALUES
    ('Stephen', 'King'),
    ('Mark', 'Twain'),
    ('Agatha', 'Christie'),
    ('Jane', 'Austen'),
    ('Ernest', 'Hemingway');

/*
 Publishers 
 */
INSERT INTO
    Publishers (publisher_name)
VALUES
    ('Scribner'),
    ('Gallery Books'),
    ('SeeWolf Press'),
    ('Dover Publications'),
    ('William Morrow'),
    ('Penguin Books'),
    ('Forgotten Books');

/*
 Books
 */
INSERT INTO
    Books (isbn, title, author_id, year, publisher_id)
VALUES
    ('978-19-8213798-4', 'If It Bleeds', 1, '2021', 1),
    ('978-15-0114741-8', 'Needful Things', 1, '2018', 2),
    ('978-1948-13282-4',
        'The Adventures of Tom Sawyer: Original Illustrations',
        2,
        '2018',
        3
    ),
    (
        '978-0486-28061-5',
        'Adventures of Huckleberry Finn',
        2,
        '1994',
        4
    ),
    (
        '978-0062-07348-8',
        'And Then There Were None',
        3,
        '2011',
        5
    ),
    (
        '978-0062-07353-2',
        'Crooked House',
        3,
        '2011',
        5
    ),
    (
        '978-0141-43951-8',
        'Pride and Prejudice',
        4,
        '2002',
        6
    ),
    (
        '978-0141-43966-2',
        'Sense and Sensibility',
        4,
        '2003',
        6
    ),
    (
        '978-0684-80335-7',
        'For Whom the Bell Tolls',
        5,
        '1995',
        1
    ),
    (
        '978-0243-32342-5',
        'A Farewell to Arms',
        5,
        '2019',
        7
    );


/*
 BookCopies 
 */
INSERT INTO
    BookCopies (book_id, location_id)
VALUES
    (1, 5),
    (1, 4),
    (2, 3),
    (3, 2),
    (3, 1),
    (4, 1),
    (4, 5),
    (5, 2),
    (6, 3),
    (6, 4),
    (7, 4),
    (8, 5),
    (9, 3),
    (10, 2),
    (10, 1);

/*
 Patrons 
 */
INSERT INTO
    Patrons (patron_first, patron_last, email)
VALUES
    ('Koko', 'Irish', 'kokoiri@egl.com'),
    ('Corbett', 'Farner', 'corbetfarn@gmail.com'),
    ('Eloise', 'Westfall', 'elwestfa@hotmail.com'),
    ('Zelenka', 'Fichter', 'ze.fichte@aol.com'),
    ('Blanche', 'Estell', 'blestell@yahoo.com');


/*
 Checkouts
 */
INSERT INTO
    Checkouts (patron_id, checkout_date, return_date)
VALUES
    (4, '2022-02-03', '2022-02-24'),
    (4, '2021-01-11', '2021-02-01'),
    (3, '2021-05-26', '2021-06-16'),
    (2, '2022-01-29', '2022-02-19'),
    (1, '2021-10-29', '2021-11-19');

/*
 CheckedBooks 
 */
INSERT INTO
    CheckedBooks (checkout_id, copy_id, returned)
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

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;