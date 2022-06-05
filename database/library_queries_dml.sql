/*/
 CS 340 Project: Spring 2022
 Group 2: Jenna Bucien & Herakles Li
 Penguin Library System
 
 Sample data manipulation queries
 */
/*
 General queries
 pages: 
 1. index.html
 2. authors.html
 3. books.html
 4. bookcopies.html
 5. patrons.html
 6. checkouts.html
 7. checkedbooks.html
 8. publishers.html
 9. locations.html
 
 
 /* ----------- AUTHORS.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE

 pages: authors.html

 */
/* Generate Initial Table View */
select author_id, author_first, author_last 
from Authors 
order by author_last asc;

/* Insert */
insert into (author_first, author_last)
values (
    %s,
    %s
  );

/* Update Get */

SELECT author_id, author_first, author_last 
FROM Authors 
WHERE author_id = %s;
  
/* Update Post */
DELETE 
FROM Authors 
WHERE author_id = %s;

/* Delete */
delete from Authors
where author_first = :author_first_name_input
  and author_last = :author_last_name_input;
 

 /* ----------- BOOKS.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 DELETE
 
 ISBN, Title, Year, Author, Publisher
 pages: books.html
 */

 /* Initial Table View*/
select Books.book_id,
Books.isbn, 
    Books.title, 
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Publishers.publisher_name,
    Books.year
from Books
    left join Authors on Books.author_id = Authors.author_id
    left join Publishers on Books.publisher_id = Publishers.publisher_id
order by Authors.author_last asc, Books.title asc;

/*Set up Dropdown author*/
  SELECT author_id, concat(author_first, ' ', author_last) as author_name 
  FROM Authors 
  ORDER BY author_last ASC

/*Set up Dropdown publisher*/
  SELECT publisher_id, publisher_name 
  FROM Publishers 
  ORDER BY publisher_name ASC

/*Books by author filter*/
SELECT author_id, concat(author_first, ' ', author_last) as author_name 
FROM Authors 
ORDER BY author_last ASC

/*Books by author table*/
select Books.book_id,
Books.isbn, 
    Books.title,
    Publishers.publisher_name,
    Books.year
from Books
    left join Authors on Books.author_id = Authors.author_id
    left join Publishers on Books.publisher_id = Publishers.publisher_id
where Authors.author_id = %s
order by Books.title asc;

/*Books by author page information*/
select concat(Authors.author_first, ' ', Authors.author_last) as author_name 
from Authors 
where Authors.author_id = %s

/* Insert dropdown author */
SELECT author_id, concat(author_first, ' ', author_last) as author_name 
FROM Authors 
ORDER BY author_last ASC

/* Insert dropdown publisher */
SELECT publisher_id, publisher_name 
FROM Publishers 
ORDER BY publisher_name ASC

/* Insert form submission  */
INSERT INTO Books (isbn, title, author_id, publisher_id, year) 
VALUES (%s, %s, %s, %s, %s);

/* Update GET */
select Books.book_id,
Books.isbn, 
Books.title,
Authors.author_id, 
Publishers.publisher_id, 
Books.year
from Books
left join Authors on Books.author_id = Authors.author_id
left join Publishers on Books.publisher_id = Publishers.publisher_id
where Books.book_id = %s;

/* Update dropdown author */
SELECT author_id, concat(author_first, ' ', author_last) as author_name 
FROM Authors 
ORDER BY author_last ASC

/* Update dropdown publisher */
SELECT publisher_id, publisher_name 
FROM Publishers 
ORDER BY publisher_name ASC

/* Update POST */
UPDATE Books 
SET isbn=%s, title=%s, author_id=%s, publisher_id=%s, year=%s 
WHERE book_id=%s;

/* Delete */
DELETE FROM Books WHERE book_id = %s


/* ----------- BOOKCOPIES.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 DELETE
 pages: bookcopies.html
 */

 /* Note: To perform BookCopies CRUD functions, users first click on a book_id in the Books table. .*/

/* Generate Initial Direct Table View */
select BookCopies.copy_id, 
Books.title,
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Locations.location_name
from Locations
    right join BookCopies on Locations.location_id = BookCopies.location_id
    inner join Books on BookCopies.book_id = Books.book_id
    inner join Authors on Books.author_id = Authors.author_id
order by Books.title asc;

/*Bookcopies from Books View of Individual Books' copies*/
SELECT bookcopies.copy_id, bookcopies.book_id, locations.location_name
FROM bookcopies
LEFT JOIN locations ON bookcopies.location_id = locations.location_id
WHERE bookcopies.book_id = %s

/*Bookcopies from Books View of Individual Books' dropdown*/
  SELECT location_id, location_name 
  FROM Locations 
  ORDER BY location_name ASC


/*Bookcopies from Books View of Individual Books' copies form submission */
  INSERT INTO BookCopies (book_id, location_id) VALUES (%s, NULL)

/*Bookcopies from Books View of Individual Books' copies dropdown form insert into database*/
  INSERT INTO BookCopies (book_id, location_id) VALUES (%s, %s);


/*Bookcopies Update*/
/* retrieve book ID info */
select Books.book_id 
from BookCopies 
INNER JOIN Books ON BookCopies.book_id = Books.book_id 
WHERE BookCopies.copy_id  = %s;

/* update GET */
SELECT BookCopies.copy_id, 
Books.book_id, 
Books.title, 
concat(Authors.author_first, ' ', Authors.author_last) as author_name, Locations.location_name
FROM BookCopies 
    LEFT JOIN Locations ON BookCopies.location_id = Locations.location_id
    INNER JOIN Books ON BookCopies.book_id = Books.book_id
    INNER JOIN Authors ON Books.author_id = Authors.author_id
WHERE BookCopies.copy_id = %s

/*update dropdown*/
SELECT location_id, location_name 
FROM Locations 
ORDER BY location_name ASC

/*update dropdown location = -1*/
UPDATE BookCopies 
SET location_id = NULL 
WHERE copy_id=%s

/*update dropdown location else*/
UPDATE BookCopies 
SET location_id = %s 
WHERE copy_id=%s


/* Delete Book Copy Get*/
select Books.book_id 
from BookCopies INNER JOIN Books ON BookCopies.book_id = Books.book_id 
WHERE BookCopies.copy_id  = %s;

/* Delete Book Copy Post*/
DELETE FROM BookCopies 
WHERE copy_id = %s


/* ----------- PATRONS.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 Patron first, Patron last, Patron email
 pages: patrons.html
 */

/* Initial Table View*/
select patron_id,
    patron_first,
    patron_last,
    email
from Patrons
order by patron_last asc;

/* Insertion */
INSERT INTO Patrons(patron_first, patron_last, email) 
VALUES (%s, %s, %s);

/* Update GET*/
SELECT patron_id, patron_first, patron_last, email 
FROM Patrons 
WHERE patron_id = %s

/* Update POST*/
update Patrons 
set patron_first = %s, patron_last = %s, email = %s 
where patron_id = %s;

/* Delete */
DELETE FROM Patrons 
WHERE patron_id = %s


/* ----------- CHECKOUTS.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 pages: checkouts.html
 */

/* SQL to Generate Intitial Checkouts Table View */
select
    Checkouts.checkout_id,
    concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name,
    Checkouts.checkout_date,
    Checkouts.return_date
from Patrons
    inner join Checkouts on Patrons.patron_id = Checkouts.patron_id
order by Checkouts.checkout_id asc;

/*Initial checkouts patron dropdown */
SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name 
FROM Patrons 
ORDER BY patron_last ASC;

/* Checkouts INSERT  POST*/
INSERT INTO Checkouts (checkout_date, return_date, patron_id) 
VALUES (%s, %s, %s) 

/* Checkouts Update GET*/
SELECT Checkouts.checkout_id, Patrons.patron_id, Patrons.patron_first, Patrons.patron_last, Checkouts.checkout_date, Checkouts.return_date 
FROM Patrons 
INNER JOIN Checkouts ON Patrons.patron_id = Checkouts.patron_id 
WHERE checkout_id = %s

/* Checkouts Update Patron dropdown*/
SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name 
FROM Patrons 
ORDER BY patron_last ASC

/* Checkouts Update GET*/
UPDATE Checkouts 
SET patron_id = %s, checkout_date=%s, return_date=%s 
WHERE checkout_id=%s



/* Checkouts DELETE - deletes entire Checkout */
DELETE FROM Checkouts WHERE checkout_id = %s


/* Generate a CheckedBooks list from a Checkout ID */
SELECT Books.title, concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name, Checkouts.checkout_date, Checkouts.return_date, CheckedBooks.returned
FROM Checkouts
INNER JOIN Patrons ON Checkouts.patron_id = Patrons.patron_id
INNER JOIN CheckedBooks ON Checkouts.checkout_id = CheckedBooks.checkout_id
INNER JOIN BookCopies ON CheckedBooks.copy_id = BookCopies.copy_id
INNER JOIN Books ON BookCopies.book_id = Books.book_id
WHERE Checkouts.checkout_id = :checkout_id_selected;


/* ----------- CHECKEDBOOKS.py QUERIES---------------
 Checkedbooks queries
 CREATE/INSERT
 READ/SELECT
 DELETE
 
 Book Title, Patron First, Patron Last, Checkout Date, Return Date, Returned
 pages: checkedbooks.html
 */

/* Note: To perform CheckedBooks CRUD functions, users first click on a checkout_id in the Checkouts table. .*/

/* Initial Table View*/
select
CheckedBooks.checked_book_id, 
BookCopies.copy_id, 
Books.title,
concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name,
Checkouts.checkout_date,
Checkouts.return_date,
CheckedBooks.returned
from Books
    inner join BookCopies on Books.book_id = BookCopies.book_id
    inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
    inner join Checkouts on Checkouts.checkout_id = CheckedBooks.checkout_id
    inner join Patrons on Patrons.patron_id = Checkouts.patron_id
order by Checkouts.checkout_date desc;

/* To checkedbooks from checkouts initial display*/
SELECT Checkedbooks.checked_book_id, BookCopies.copy_id, Books.title, Locations.location_name, Checkouts.checkout_date, Checkouts.return_date, CheckedBooks.returned
FROM Checkouts
INNER JOIN CheckedBooks ON Checkouts.checkout_id = CheckedBooks.checkout_id
INNER JOIN BookCopies ON CheckedBooks.copy_id = BookCopies.copy_id
LEFT JOIN Locations ON BookCopies.location_id = Locations.location_id
INNER JOIN Books ON BookCopies.book_id = Books.book_id
WHERE Checkouts.checkout_id = %s
ORDER BY Books.title ASC;

/* To checkedbooks from checkouts patron query*/
SELECT concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name
FROM Patrons
INNER JOIN Checkouts ON Patrons.patron_id = Checkouts.patron_id 
WHERE Checkouts.checkout_id = %s

/*Dropdown of all book copies not in checkout*/
SELECT BookCopies.copy_id,
concat(Books.title, ' by ', Authors.author_first, ' ', Authors.author_last, ' at ', Locations.location_name, ' (Copy ID: ', BookCopies.copy_id, ')') as book_entry
FROM BookCopies
INNER JOIN Locations ON BookCopies.location_id = Locations.location_id
INNER JOIN Books ON BookCopies.book_id = Books.book_id
INNER JOIN Authors ON Books.author_id = Authors.author_id
LEFT JOIN CheckedBooks ON CheckedBooks.copy_id = BookCopies.copy_id
LEFT JOIN Checkouts ON CheckedBooks.checkout_id = Checkouts.checkout_id
WHERE Checkouts.checkout_id IS NULL 
OR 
(Checkouts.checkout_id != %s
AND 
BookCopies.copy_id NOT IN 
    (SELECT BookCopies.copy_id FROM BookCopies INNER JOIN Locations ON BookCopies.location_id = Locations.location_id
    INNER JOIN Books ON BookCopies.book_id = Books.book_id
    INNER JOIN Authors ON Books.author_id = Authors.author_id
    INNER JOIN CheckedBooks ON CheckedBooks.copy_id = BookCopies.copy_id
    INNER JOIN Checkouts ON CheckedBooks.checkout_id = Checkouts.checkout_id
    WHERE Checkouts.checkout_id = %s)
)
GROUP BY BookCopies.copy_id
ORDER BY Books.title asc
;

/* Insertion */
INSERT INTO CheckedBooks (checkout_id, copy_id, returned) VALUES (%s, %s, %s);

/* Update display book*/
select checkout_id from checkedbooks where checked_book_id = %s;

/* Update display book GET*/
SELECT returned from checkedbooks where checked_book_id = %s;

/* Update display book POST*/
update Checkedbooks set returned = %s where checked_book_id = %s;


/* Delete checkedbook info */
select checkout_id 
from checkedbooks 
where checked_book_id = %s;

/* Delete checkedbook */
DELETE FROM checkedbooks 
WHERE checked_book_id = %s


/* ----------- PUBLISHERS.py QUERIES---------------
  /*
  Publishers queries
  CREATE/INSERT
  READ/SELECT
  UPDATE
  DELETE
  
  pages: publishers.html
  */

/* Generate Intitial Table View */
select publisher_id,
publisher_name
from Publishers
order by Publishers.publisher_name asc;

/* Insert Publishers */
INSERT INTO Publishers(publisher_name) 
VALUES (%s);

/* Update Publishers GET */
SELECT publisher_name 
FROM Publishers 
WHERE publisher_id = %s

/* Update Publishers POST */
update Publishers 
set publisher_name = %s 
where publisher_id = %s;
  
/* Delete Publishers */
DELETE FROM Publishers 
WHERE publisher_id = %s


/* ----------- LOCATIONS.py QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 location name, location address 
 pages: locations.html
 */

 /* Initial Table View*/
select location_id,
location_name,
location_address
from Locations
order by location_id asc;

/* Insertion */
INSERT INTO Locations(location_name, location_address) 
VALUES (%s,%s);

/* Update GET*/
SELECT location_name, location_address 
FROM Locations 
WHERE location_id = %s

/* Update Post*/
update Locations 
set location_name = %s, location_address = %s 
where location_id = %s;


/* Delete */
DELETE FROM Locations 
WHERE location_id = %s

