/*
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
 
 
 /* ----------- AUTHORS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 pages: authors.html
 */
/* Generate Initial Table View */
select author_first,
  author_last
from Authors
order by author_last asc;
/* Insert */
insert into (Authors.first_name, Authors.last_name)
values (
    :author_first_name_input,
    :author_last_name_input
  );
/* Update */
select author_id
from Authors
where author_first = :author_first
  and author_last = :author_last;
/* capture the author_id found as :author_id_var */
update Authors
set author_first = :author_first_name_input,
  author_last = :author_last_name_input
where author_id = :author_id_var;
/* Delete */
delete from Authors
where author_first = :author_first_name_input
  and author_last = :author_last_name_input;
/*
 
 /* ----------- BOOKS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 
 pages: books.html
 */
/* ----------- BOOKCOPIES QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 pages: bookcopies.html
 */
/* Generate Initial Table View */
select Books.title,
  Authors.author_first,
  Authors.author_last,
  Locations.location_name
from Locations
  inner join BookCopies on Locations.location_id = BookCopies.location_id
  inner join Books on BookCopies.book_id = Books.book_id
  inner join Authors on Books.author_id = Authors.author_id
order by Books.title asc;
/* ----------- PATRONS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 DELETE
 
 pages: patrons.html
 */
/* ----------- CHECKOUTS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 UPDATE
 
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
/* ----------- CHECKEDBOOKS QUERIES---------------
 Checkedbooks queries
 CREATE/INSERT
 READ/SELECT
 DELETE
 
 pages: checkedbooks.html
 */
/* ----------- PUBLISHERS QUERIES---------------
 /*
 Publishers queries
 CREATE/INSERT
 READ/SELECT
 
 pages: publishers.html
 */
/* SQL to Generate Intitial Table View */
select Publishers.publisher_name
from Publishers
order by Publishers.publisher_name asc;
/* SQL to Insert New Publisher */
insert into Publishers (Publishers.publisher_name)
values (:publisher_name_input);
/* ----------- LOCATIONS QUERIES---------------
 CREATE/INSERT
 READ/SELECT
 
 pages: locations.html
 */