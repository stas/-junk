#!/usr/bin/env python
"""
A syntax checker for a python alike programming language
See main.lang file for source code example
The checker must generate the codes table and table of symbols for current source file
"""
import sys
import re
from pprint import pprint

def checker(text):
    """
    This will check <text> for syntax rules
    It uses regular expression package <re>
    <pattern> has a set of regex definitions that has to match the atoms.
    Since this is a generator, it will return the matching atoms along with their value
    On failure it will output the position in the <text> where pattern fails matching
    """
    pattern = re.compile(r"""
        (?P<reserved_key>[A-Z_][A-Z0-9_]*)
        |(?P<identifier>[a-zA-Z][a-zA-Z0-9_]+)
        |(?P<digits>[0-9]+)
        |(?P<string>\'[a-zA-Z0-9_(.)]+\')
        |(?P<array>\[(\'(\d+)|(\w+)|(.)+\')\])
        |(?P<newline>\n)
        |(?P<whitespace>\s+)
        |(?P<special_char>([=][=])|([<][=])|([>][=])|[<]|[>]|[+]|[-]|[*]|[/]|[=])
        |(?P<match>[=][=])
        |(?P<less_then>[<][=])
        |(?P<more_then>[>][=])
        |(?P<less>[<])
        |(?P<more>[>])
        |(?P<plus>[+])
        |(?P<minus>[-])
        |(?P<times>[*])
        |(?P<division>[/])
        |(?P<equals>[=])
        """, re.VERBOSE)
    
    pos = 0
    
    while True:
        ok = pattern.match(text, pos)
        if not ok:
            break
        pos = ok.end()
        atomname = ok.lastgroup
        atomvalue = ok.group(atomname)
        yield atomname, atomvalue
    if pos != len(text):
        print 'Syntax error at ', pos, ' of ', len(text)

def gen_table(data):
    """
    Check if <data> suid our simbol table and return an array with its code and simbol value
    """
    type = data[0]
    value = data[1]
    
    ts = dict(
        reserved_key = -1,
        identifier = 0,
        string = 1,
        digits = 2,
        array = 3,
        )
    
    if type is not 'whitespace' or 'special_char' or 'newline':
        if ts.has_key(type):
            return ts.get(type), value


# Start checking...
def main():
    """
    Starter for our sytax chcker.
    First argument will be taken as a filename to be checked
    This will parse the <file> and call checker() for each line
    Before each call, the <line> number will be outputed.
    """
    tc = list()
    st = list()
    
    file = None
    
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        print 'Usage: ', sys.argv[0], '<source file to check>'
        sys.exit(0)
    
    print 'Checking ', file, '...'
    
    file_h = open(file, "r")
    lines = file_h.readlines()
    curr_line = 1
    for l in lines:
        print 'Checking line: ', curr_line
        for r in checker(l):
            atom = gen_table(r)
            if atom:
                st.append(r[1])
                tc.append(atom)
        curr_line += 1
    st = list(set(st))
    
    print
    print 'Printing TC'
    print '###########'
    for item in st:
        # position in tc and position in st
        for code in tc:
            if code[1] is item:
                print code[0], st.index(item)
    
    print
    print 'Printing ST'
    print '###########'
    for simbol in st:
        print st.index(simbol), simbol
    
    # For debugging, print the not joined TC
    #pprint(tc)

if __name__ == "__main__":
    main()
