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
update Authors
set author_first = :author_first_name_input,
  author_last = :author_last_name_input
where author_id = (
    select author_id
    from Authors
    where author_first = :author_first_selected
      and author_last = :author_last_selected
  );
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
 DELETE
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
/* Generate List of Books Currently On Shelf */
select Books.title,
  Authors.author_first,
  Authors.author_last,
  Locations.location_name
from Locations
  inner join BookCopies on Locations.location_id = BookCopies.location_id
  inner join Books on BookCopies.book_id = Books.book_id
  inner join Authors on Books.author_id = Authors.author_id
where Locations.location_name IS NOT NULL
order by Books.title asc;
/* Generate List of Books Currently Checked Out (i.e. Location is NULL)
 with Return Dates
 */
select Books.title,
  Checkouts.return_date
from Locations
  inner join BookCopies on Locations.location_id = BookCopies.location_id
  and Locations.location_name is null
  inner join Books on BookCopies.book_id = Books.book_id
  inner join Authors on Books.author_id = Authors.author_id
  inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
  inner join Checkouts on CheckedBooks.checkout_id = Checkouts.checkout_id
)
order by Books.title asc;
/* Create New Book Copy By Searching for Book ISBN. If ISBN is not found, redirect person to Create New Book Table */
select book_id
from Books
where isbn = :isbn_input;
/* if book_id found from isbn, search location id based on location name  */
select location_id
from Locations
where location.location_name = :location_name_input;
/* insert into BookCopies */
insert into BookCopies (book_id, location_id)
values (:book_id, :location_id);
/* Delete Book Copy */
delete from BookCopies
where book_copy_id = :book_copy_selected_from_table;

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

/* ----------- CHECKEDBOOKS QUERIES---------------
 Checkedbooks queries
 CREATE/INSERT
 READ/SELECT
 DELETE
 
 pages: checkedbooks.html
 */
select
  /* I was thinking that maybe we should have /checkedbooks.html redirect from clicking on a checkout_id from the Checkouts table. Then it still counts as a separate page. So, a user would first add a Checkout. Then, the checkout would appear on the table. Then, the user would click on the Checkout id in the table and add CheckedBooks from there.*/

  /* ----------- PUBLISHERS QUERIES---------------
   /*
   Publishers queries
   CREATE/INSERT
   READ/SELECT
   
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
 
 pages: locations.html
 */