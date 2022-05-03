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


 */


show tables;
select * from authors;
select * from books;
select * from bookcopies;
select * from checkouts;
select * from locations;
select * from checkedbooks;
select * from patrons;
select * from publishers;

/*
Authors queries
CREATE/INSERT
READ/SELECT

pages: authors.html
 */


/*
Books queries
CREATE/INSERT
READ/SELECT

pages: books.html
 */


/*
Bookcopies queries
CREATE/INSERT
READ/SELECT

pages: bookcopies.html
 */


/*
Patrons queries
CREATE/INSERT
READ/SELECT
UPDATE
DELETE

pages: patrons.html
 */


 /*
Checkouts queries
CREATE/INSERT
READ/SELECT
UPDATE

pages: checkouts.html
 */
 
/* SQL to Generate Intitial Table View */
select Patrons.patron_first, Patrons.patron_last, Checkouts.checkout_date, Checkouts.return_date
from Patrons
inner join Checkouts on Patrons.patron_id = Checkouts.patron_id
order by Checkouts.checkout_date desc;

/* Checkouts INSERT */
insert into Checkouts (




  /*
Checkedbooks queries
CREATE/INSERT
READ/SELECT
DELETE

pages: checkedbooks.html
 */


 /*
Publishers queries
CREATE/INSERT
READ/SELECT

pages: publishers.html
 */
 
/* SQL to Generate Intitial Table View */
select Publishers.publisher_name from Publishers
order by Publishers.publisher_name asc;

/* SQL to Insert New Publisher */
insert into Publishers (Publishers.publisher_name)
values (:publisher_name_input);



  /*
Locations queries
CREATE/INSERT
READ/SELECT

pages: locations.html
 */