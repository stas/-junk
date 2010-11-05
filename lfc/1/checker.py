#!/usr/bin/env python

import sys
import re

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
        |(?P<if_operator>(IF)|(if))
        |(?P<else_operator>(ELSE)|(else))
        |(?P<endif_operator>(ENDIF)|(endif))
        |(?P<while_operator>(WHILE)|(while))
        |(?P<endwhile_operator>(ENDWHILE)|(endwhile))
        |(?P<identifier>[A-Z_][A-Z0-9_]*)
        |(?P<variable>[a-zA-Z][a-zA-Z0-9_]+)
        |(?P<digits>[0-9]+)
        |(?P<string>\'[a-zA-Z0-9_(.)]+\')
        |(?P<array>\[(\'(\d+)|(\w+)|(.)+\')\])
        |(?P<newline>\n)
        |(?P<whitespace>\s+)
        |(?P<match>[=][=])
        |(?P<less_then>[<][=])
        |(?P<more_then>[<][=])
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

# Start checking...
def main():
    """
    Starter for our sytax chcker.
    First argument will be taken as a filename to be checked
    This will parse the <file> and call checker() for each line
    Before each call, the <line> number will be outputed.
    """
    file = "main.lang"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    
    print 'Checking ', file, '...'
    
    file_h = open(file, "r")
    lines = file_h.readlines()
    curr_line = 1
    for l in lines:
        print 'Checking line: ', curr_line
        for r in checker(l):
            print r
        curr_line += 1
        print

if __name__ == "__main__":
    main()