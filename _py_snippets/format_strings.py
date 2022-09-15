
def transform_string( st ):
    s = str(st)

    if ( s.startswith( '"' ) and not s.endswith( '"' ) ) or ( s.startswith( "'" ) and not s.endswith( "'" ) ):
        print( f"ERROR: the string doesn't meet the string format -- received {s}" )
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

def transform( st ):
    print( "(%s) %s -> (string) %s" % (type(st), st, transform_string(st)) )

transform( "'this is a string'" )
transform( "''" )
transform( "" )
transform( '"this is a string"' )
transform( '""' )
transform( 4 )
transform( 4.4 )
transform( '"4.4"' )
try:
    transform( "'s\"" )
except SyntaxError:
    print( "syntax error (%s)" % "'s\"" )
try:
    transform( "'s" )
except SyntaxError:
    print( "syntax error (%s)" % "'s" )