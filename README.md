
# CSV to SQL -- project README

## What is this?

This is a tiny tool, quickly written in Python, developed mostly as exercise for practising some complex uncommon feature of Python. 

The tool takes some data from a table written in Csv, processes it and creates a SQL file containing

- a basic `CREATE TABLE` statement (the program will have a minimal capability of types understanding)
- a list of `INSERT INTO` statements, one for each line
- and other useful statements, in case

## INPUT FILE -- a example of CSV input file

### Simple file 1

This file doesn't contain any metadata. Here are the characteristics of this file:

- 6 columns: INT, INT, INT, INT , VARCHAR, VARCHAR
- the fourth column contains a NULL value

```text
1,2,3,44,"5",'6'
1,2,33,4,"5",'66'
1,22,3,4,,'666'
11,2,3,,"5",'66'
```

The expected SQL output is the following:

- columns as labeled following the spreadsheets convention
- the program can understand the type of each column
- the name of the input file is used when not specified a name for the table

```sql
CREATE TABLE input_sample_1 (
    A INTEGER,
    B INTEGER,
    C INTEGER,
    D INTEGER, 
    E VARCHAR(1),
    F VARCHAR(3)
)

INSERT INTO input_sample_1 VALUES ( 1, 2, 3, 44, '5', '6' )
INSERT INTO input_sample_1 VALUES ( 1, 2, 33, 4, '5', '66' )
INSERT INTO input_sample_1 VALUES ( 1, 22, 3, 4, NULL, '666' )
INSERT INTO input_sample_1 VALUES ( 11, 2, 3, NULL, '5', '66' )
```