
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
'''

import os
import sys

def log( s ):
    ''' print a message on the screen with identifier
    '''

    print( "[read_csv] ", str(s) )


def read_csv_file( path ):
    '''open and read the CSV file

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
    slist = list( flp )

    # and close it
    flp.close( )

    return slist


def main( ):
    ''' the main of the test
    '''

    log( "reading file" )
    l = read_csv_file( '../test_codes/input_sample_1.csv' )
    log( "the file is:\n---" )
    for ln in l:
        print(ln, end='')
    print( "\n---" )

    log( "splitting lines" )
    lsplit = []
    for ln in l:
        lsplit.append(
                tuple([ s.strip() for s in ln.rsplit(sep=",")])
                )
    log( "the new structure of the file:" )
    for ln in lsplit:
        print( ln )


if __name__ == "__main__":
    main( )