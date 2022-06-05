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
/*
 

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
ELECT author_id, concat(author_first, ' ', author_last) as author_name 
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


/* ----------- PATRONS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 Patron first, Patron last, Patron email
 pages: patrons.html
 */

/* Initial Table View*/
 select patron_first,
patron_last,
email
 from Patrons
 order by patron_last asc;


/* Insertion */
insert into Patrons(patron_first, patron_last, email)
values(
:patron_first_input,
:patron_last_input,
:email_input
);

/* Update */
update Patrons
set patron_first = :patron_first_input,
	patron_last = :patron_last_input,
    email = :email_input
where patron_id = (
	select patron_id
    from Patrons
    where patron_first = :patron_first_input,
	and patron_last = :patron_last_input,
    and email = :email_input
    );

/* Delete */
delete from Patrons
    where patron_first = :patron_first_input,
	and patron_last = :patron_last_input,
    and email = :email_input;


/* ----------- CHECKOUTS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 pages: checkouts.html
 */

/* SQL to Generate Intitial Checkouts Table View */
select Patrons.patron_first,
  Patrons.patron_last,
  Checkouts.checkout_date,
  Checkouts.return_date
from Patrons
  inner join Checkouts on Patrons.patron_id = Checkouts.patron_id
order by Checkouts.checkout_date desc;

/* Checkouts INSERT */
/* get patron_id from patron's name */
select patron_id
from Patrons
where patron_first = :patron_first_input
  and patron_last = :patron_last_input;
/* insertion */
insert into Checkouts (checkout_date, return_date, patron_id)
values (
    :checkout_date_input,
    :return_date_input,
    :patron_id_found_from_select_query
  )

/* Checkouts UPDATE - allow for change of checkout date, return date, patron. Books checked out changed through CheckedBooks. */
/* get patron_id from patron's name */
select patron_id
from Patrons
where patron_first = :patron_first_input
  and patron_last = :patron_last_input;
/* update */
update Checkouts
set patron_id = :patron_id_found_from_select_query,
  checkout_date = :checkout_date_input,
  return_date = :return_date_input
where checkout_id = :checkout_id_selected;

/* Checkouts DELETE - deletes entire Checkout */
delete from Checkouts
where checkout_id = :checkout_id_selected;


/* Generate a CheckedBooks list from a Checkout ID */
SELECT Books.title, concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name, Checkouts.checkout_date, Checkouts.return_date, CheckedBooks.returned
FROM Checkouts
INNER JOIN Patrons ON Checkouts.patron_id = Patrons.patron_id
INNER JOIN CheckedBooks ON Checkouts.checkout_id = CheckedBooks.checkout_id
INNER JOIN BookCopies ON CheckedBooks.copy_id = BookCopies.copy_id
INNER JOIN Books ON BookCopies.book_id = Books.book_id
WHERE Checkouts.checkout_id = :checkout_id_selected;


/* ----------- CHECKEDBOOKS QUERIES---------------
 Checkedbooks queries
 CREATE/INSERT
 READ/SELECT
 DELETE
 
 Book Title, Patron First, Patron Last, Checkout Date, Return Date, Returned
 pages: checkedbooks.html
 */

/* Initial Table View*/
select Books.title,
Patrons.patron_first,
Patrons.patron_last,
Checkouts.checkout_date,
Checkouts.return_date,
CheckedBooks.returned

from Books
  inner join BookCopies on Books.book_id = BookCopies.book_id
  inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
  inner join Checkouts on Checkouts.checkout_id = CheckedBooks.checkout_id
  inner join Patrons on Patrons.patron_id = Checkouts.patron_id
order by Checkouts.checkout_date desc;

/* Insertion */
insert into CheckedBooks (checkout_id, copy_id, returned)
values (
  :checkout_id_input,
  :copy_id_input,
  0
);

/* Update */
update CheckedBooks
set returned = :return_date_input
where CheckedBooks_id = :checkedbooks_id_input;

/* Delete */
delete from CheckedBooks
where CheckedBooks_id = :checkedbooks_id_input;


  /* I was thinking that maybe we should have /checkedbooks.html redirect from clicking on a checkout_id from the Checkouts table. Then it still counts as a separate page. So, a user would first add a Checkout. Then, the checkout would appear on the table. Then, the user would click on the Checkout id in the table and add CheckedBooks from there.*/


/* ----------- PUBLISHERS QUERIES---------------
  /*
  Publishers queries
  CREATE/INSERT
  READ/SELECT
  UPDATE
  DELETE
  
  pages: publishers.html
  */

/* Generate Intitial Table View */
select Publishers.publisher_name
from Publishers
order by Publishers.publisher_name asc;

/* Insert Publishers */
insert into Publishers (publisher_name)
values (:publisher_name_input);

/* Update Publishers */
update Publishers
set publisher_name = :publisher_name_input
where author_id = (
    select publisher_id
    from Publishers
    where publisher_name = :publisher_name_selected
  );
  
/* Delete Publishers */
delete from Publishers
where publisher_name = :publisher_name_selected;


/* ----------- LOCATIONS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 location name, location address 
 pages: locations.html
 */

 /* Initial Table View*/
 select location_name,
 location_address
 from Locations
 order by location_name asc;

/* Insertion */
insert into Locations(location_name, location_address)
values (
:location_name_input,
:location_address_input
);

/* Update */
update Locations
set location_name = :location_name_input,
	location_address = :location_address_input
where location_id = (
	select location_id
    from Locations
    where location_name = :location_name_input
	and location_address = :location_address_input
    );
/* Delete */
delete from Locations
where location_name = :location_name_input
	or location_address = :location_address_input;

