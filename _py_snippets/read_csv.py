
''' TEST : read a simple CSV

What does it mean read?
- extract the rows of the file
- split the lines to get a matrix of values
- each value is formatted as string, as it comes from the reading phase

Checkings:
- the num of colums must be the same for each line of the file

Note: 
    **development phases**
    1. (DONE) read the file and print on the screen
    2. (DONE) split lines
    3. (DONE) preprocessing step: formatting strings from "str" to 'str'.
        implement the method to perform the transformation
    4. (DONE) minimal types understanding on one value
        recognize between integers and strings
    5. (DONE) type understanding on the entire table
    6. (DONE) SQL statement production
    7. write statements on file
'''

import os
import sys

def log( s ):
    ''' print a message on the screen with identifier
    '''

    print( "[read_csv] ", str(s) )


def read_csv_file( path ):
    '''open and read the CSV file

    the function reads and splits the fields of the CSV file.

    Arguments:
        path (string) : 
            the complete path of the file. It can be relative or also absolute

    Returns:
        a list of lines from the file, not yet splitted
    '''

    slist = []

    # try open the file
    flp = None
    path = os.path.realpath(path)
    try:
        flp = open( path, 'r' )
    except FileNotFoundError as e:
        log( f"file not found -- {path}" )
    except Exception as e:
        log( f"another exception occurred \n---\n{str(e)}\n---" )

    # read the file
    # slist = list( flp )
    len_row = -1
    idx = 0
    for ln in flp:
        # split the line
        ln = [ s.strip() for s in ln.rsplit(sep=",") ]

        # check its len
        if len_row < 0:
            len_row = len( ln )
        elif len_row != len( ln ):
            log( f"ERROR: found a line with different len -- expected: {len_row} -- found: {len(ln)} at {idx}" )
        
        # confirm the line 
        slist.append( ln )
        idx = idx + 1

    # and close it
    flp.close( )

    return slist


def transform_string( st ):
    ''' transform a string from "str" to 'str'

    this method transforms a string from a double-quoted format
    to a single-quoted format. "str" becomes 'str'.

    The method also checks the format of the string:
    - A exception is raised when the string has two different types of quotes

    Parameters:
        st (string):
            the string to check and format

    Returns:
        (string) the string transformed, or None in case it represents
        a null value. 
    
    Raises:
        SyntaxError : 
            the string doesn't meet the format rules
    
    Note:
        a string starts with a single quote or a double quote. 
        If not, the method simply casts the value to string and
        returns this castes value, stripped. 
    '''

    s = str(st)

    if ( s.startswith( '"' ) and not s.endswith( '"' ) ) or ( s.startswith( "'" ) and not s.endswith( "'" ) ):
        log( f"ERROR: the string doesn't meet the string format -- received {s}" )
        raise SyntaxError()
    
    if s == '':
        return None
    elif s.startswith('"'):
        r = "'" + s[1:len(s)-1] + "'"
        if r == "\'\'":
            return None
        else:
            return r
    elif s == "''":
        return None
    else:
        return s


def understand_type_value( val ):
    ''' recognize the type of the value

    this method uses simple python functions in order to understand
    the type of a value provided by argument. 

    Types recognized:
    - INTEGER -- isdigit -- 1234 , 3, -3635
    - FLOAT -- isfloat -- 66666.7777 , 124.237426387426
    - VARCHAR -- starts with ' -- 'a string'

    Note: 
        for what concerns the strings, the VARCHAR is returned without
        a len, because it should be provided by another processing phase.
    
    Note:
        in absence of a precise order, everything is recognized as a string. 
    
    Note:
        for what concerns the float values, the format must be of type 
        *7122.33* and not, for instance *7,122.33* or *7.122,33*; a first
        formatting is needed. 
    
    Parameters:
        val (string) : 
            the value to "understand"
    
    Returns:
        (string) the type as uppercase string
    '''

    st = str(val)
    if st.startswith( '-' ):
        st = st[1:]

    # it's super easy to detect a string following the format
    if st.startswith("'"):
        return 'VARCHAR'
    
    if '.' in st:
        # check if it contains more than one point
        if st.find('.') != st.rfind('.'):
            log( "unable to cast number! -- received %s" % st )
            raise SyntaxError( )
        
        # if the check has been passed, the num is a float
        return 'FLOAT'
    
    if st.isdigit( ):
        return 'INTEGER'
    
    # unknown type
    log( f"ERROR: unknown type! -- received '{val}'" )
    raise SyntaxError( )



def understand_col_type( tab, colno ):
    ''' understand the types for each column of the table

    Parameters:
        col (list of strings) :
            the column as a list
    
    Returns:
        tab (list of list of strings):
            the dataset
        colno (int):
            the column index

    Note:
        if one value is recognized as FLOAT, the entire data type 
        becomes FLOAT.
    '''

    # data
    null_possible = False
    main_datatype = ""
    max_str_len = 0

    #for tp in col:
    for i in range(len(tab)):
        tp = tab[i][colno]

        # check for None types
        if tp is None:
            # print( "NONE found at %i, %i" % (i, colno) )
            null_possible = True
            # print( "null_possible: ", str(null_possible) )
            continue
        
        # check main datatype if possible
        if main_datatype == "":
            main_datatype = understand_type_value( tp )
            continue
        
        # for varchars only, check che max len
        if main_datatype == 'VARCHAR':
            if len(tp) > max_str_len:
                max_str_len = len(tp)
            continue
        
        # also check if the integer has to be converted in float
        if main_datatype == 'INTEGER' and understand_type_value( tp ) == 'FLOAT':
            main_datatype = 'FLOAT'
    
    # write the statement
    sql_statement = []
    
    if main_datatype == 'VARCHAR':
        sql_statement.append( main_datatype + '(' + str(max_str_len) + ')' )
    else:
        sql_statement.append( main_datatype )

    if not null_possible:
        sql_statement.append( "NOT NULL" )
    
    return sql_statement


def sql_create_table( tabname, tabncolnames, tabparams, format=True, semicolon=True ):
    ''' create the CREATE TABLE statement

    Arguments:
        tabname (string):
            the name of the table
        tabcolnames (list of strings):
            names of the columns
        tabparams (list of lists of strings):
            the parameters, one row for each column
        format (boolean, default True):
            if true, the SQL statement will contain the special 
            characters, otherwise the statement is print on one 
            unique line. 
        semicolon (bool, default True):
            if true, the semicolon is added at the end 
            of the SQL statement
    
    Returns:
        (string) the SQL statement
    '''

    # statement first part
    sql = "CREATE TABLE " + tabname + " ( "
    if format:
        sql = sql + "\n"
    
    # statement body
    for i in range(len(tabncolnames)):
        # data
        ln = tabparams[i]
        col = tabncolnames[i]

        if format:
            sql = sql + "\t"
        
        sql = sql + col + " "
        for j in range(len(ln)):
            sql = sql + ln[j]
            if j < len(ln)-1:
                sql = sql + " "
            elif i < len(tabncolnames)-1:
                sql = sql + ","
        
        if format:
            sql = sql + "\n"
        else:
            sql = sql + " "

    # statement end
    sql = sql + ")"
    if semicolon:
        sql = sql + ";"

    return sql


def sql_insert_into( tabname, record, types, format=True, semicolon=True, force_single_quote=True ):
    '''get a record as SQL INSERT INTO statement

    Parameters:
        tabname (string):
            the name of the table
        record (list of strings):
            the rows of the CSV file
        types: (list of lists of strings)
            the SQL chatacterization of the columns
        format (boolean, default True):
            if true, the SQL statement will contain the special 
            characters, otherwise the statement is print on one 
            unique line. 
        semicolon (bool, default True):
            if true, the semicolon is added at the end 
            of the SQL statement
        force_single_quote (bool, default True):
            enclose each field between single quotes
    
    Returns:
        the SQL statement as string
    '''

    sql = "INSERT INTO " + tabname + " VALUES ( "
    if format:
        sql = sql + "\n"
    
    for i in range(len(record)):
        if format: sql = sql + "\t"
        field = str(record[i])
        if force_single_quote and not field.startswith("'"):
            field = "'" + field + "'"
            
        sql = sql + field
        if i < len(record)-1:
            sql = sql + ", "
            if format: sql = sql + "\n"
    
    if format: 
        sql = sql + "\n"
    else:
        sql = sql + " "
    
    sql = sql + ")"
    if semicolon:
        sql = sql + ";"
    
    return sql



def write_sql_file( outpath, tabname, tabcolnames, tabparams, tabrecords, semicolon=True, force_single_quote=True ):
    ''' write the SQL representation of the CSV on file

    Parameters:
        outpath (string):
            the path of the output file, also relative
        tabname (string):
            the name of the table
        tabcolnames (list of string):
            names of the columns of the file
        tabparams (list of lists of strings):
            from types understanding process
        tabrecords (list of lists of strings):
            the dataset
        semicolon (bool, default True):
            if true, the semicolon is added at the end 
            of the SQL statement
        force_single_quote (bool, default True):
            enclose each field between single quotes
    
    Returns:
        true if the operation succeeded
    '''

    # generate the SQL code
    sql = sql_create_table( tabname, tabcolnames, tabparams, True, semicolon )
    for record in tabrecords:
        sql = sql + "\n" + sql_insert_into( tabname, record, tabparams, False, semicolon, force_single_quote )
    
    # write the code on file
    # print( sql )
    flp = None
    try:
        flp = open( os.path.realpath( outpath ), 'w' )
    except Exception:
        log( "ERROR: unable to open the file in write mode" )
    
    flp.write( sql )
    flp.close( )








    



    

    



    



def main( ):
    ''' the main of the test
    '''

    log( "reading file" )
    lsplit = read_csv_file( '../test_codes/input_sample_1.csv' )
    log( "the file is:" )
    print("---")
    for ln in lsplit:
        print(ln)
    print( "\n---" )


    log( 'table transformation' )
    for i in range( len( lsplit ) ):
        for j in range( len(lsplit[0]) ):
            lsplit[i][j] = transform_string( lsplit[i][j] )
    print("---")
    for ln in lsplit:
        print( ln )
    print("---")


    log( 'table types understanding' )
    print("---")
    types = []
    for colno in range( len( lsplit[0] ) ):
        types.append( understand_col_type( lsplit, colno ) )
        print( types[colno] )
    print("---")


    log( 'create table statement' )
    tabcolnames = ['A','B','C','D','E','F']
    tabname = 'input_sample_1'
    print("---")
    print( sql_create_table( tabname, tabcolnames, types ) )
    for record in lsplit:
        print(sql_insert_into( tabname, record, types, format=False, force_single_quote=True ))
    print("---")
    log( "writing file..." )
    write_sql_file( "../test_codes/pysql_test.sql", tabname, tabcolnames, types, lsplit )

    log("Done.")
    

    


if __name__ == "__main__":
    main( )