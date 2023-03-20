with top_countries as (select id from books_country limit 10),
 top_books as (select id from books_book limit 10)
select * from books_book where country_id in (select id from top_countries) and id in (select id from top_books);
