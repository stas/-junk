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
        (?P<read_operator>(READ)|(read))
        |(?P<print_operator>(PRINT)|(print))
        |(?P<const_def>(CONST)|(const))
        |(?P<var_def>(VAR)|(var))
        |(?P<if_operator>(IF)|(if))
        |(?P<else_operator>(ELSE)|(else))
        |(?P<endif_operator>(ENDIF)|(endif))
        |(?P<while_operator>(WHILE)|(while))
        |(?P<endwhile_operator>(ENDWHILE)|(endwhile))
        |(?P<reserved_key>[A-Z_][A-Z0-9_]*)
        |(?P<identifier>[a-zA-Z][a-zA-Z0-9_]+)
        |(?P<digits>[0-9]+)
        |(?P<string>\'[a-zA-Z0-9_(.)]+\')
        |(?P<array>\[(\'(\d+)|(\w+)|(.)+\')\])
        |(?P<newline>\n)
        |(?P<whitespace>\s+)
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
        read_operator = 4,
        print_operator = 5,
        if_operator = 6,
        endif_operator = 7,
        else_operator = 8,
        while_operator = 9,
        endwhile_operator = 10,
        plus = 11,
        times = 12,
        minus = 13,
        less = 14,
        more = 15,
        newline = 16,
        whitespace = 17,
        match = 18,
        less_then = 19,
        more_then = 15,
        division = 21,
        equals = 22,
        const_def = 23,
        var_def = 24,
        )
    
    if ts.has_key(type) and type not in ['whitespace', 'newline']:
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

    #pprint(tc)
    #pprint(st)

    print
    print 'Printing PIF'
    print '###########'
    for item in st:
        # position in tc and position in st
        for code in tc:
            if code[1] is item:
                print st.index(item), code[0]
                if code[0] > 3:
                    st[st.index(item)] = None
    
    print
    print 'Printing ST'
    print '###########'
    seen = set()
    for simbol in st:
        if simbol and simbol not in seen:
            seen.add(simbol)
            print st.index(simbol), simbol
    
if __name__ == "__main__":
    main()
