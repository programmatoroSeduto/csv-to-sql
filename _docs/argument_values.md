
# Command Line Arguments

General:

- configuration file path

SQL output:

- minimum varchar threshold

    by default, a string is rendered as `VARCHAR()` choosing as length the maximum one. You can fix a min length for `VARCHAR` manually if you need to do it

- add not null
  
  the user can decide if to add the `NOT NULL` statement when possible. The statement is added only if the column does contain no `NULL` value inside

- force not null -- allow null values
  
  a little fidderent from the previous one: the option makes the program to terminate when a `NULL` value is identified inside the table. Each colums is forced to be `NOT NULL`.

- out table name

  the name of the table inside the SQL statement; the name of the file is used in case

- don't use VARCHAR
  
  use `CHAR()` instead of `VARCHAR()`