CREATE TABLE input_sample_1 ( 
	A INTEGER NOT NULL,
	B INTEGER NOT NULL,
	C INTEGER NOT NULL,
	D FLOAT,
	E VARCHAR(3),
	F VARCHAR(5) NOT NULL
);
INSERT INTO input_sample_1 VALUES ( '1', '2', '3', '4.4', '5', '6' );
INSERT INTO input_sample_1 VALUES ( '1', '2', '33', '4', '5', '66' );
INSERT INTO input_sample_1 VALUES ( '1', '22', '3', '4', 'None', '666' );
INSERT INTO input_sample_1 VALUES ( '11', '2', '3', 'None', '5', '66' );