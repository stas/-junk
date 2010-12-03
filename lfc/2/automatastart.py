#!/usr/bin/env python

import sys
from automata.logic import Logic

def main():
    option = None
    
    if len(sys.argv) > 1:
        option = int(sys.argv[1])
    else:
        print 'Usage: ', sys.argv[0], '<option ID>'
        print '''
    ID|Option description
    -----------------------
    1 |Read finite automata from file
    2 |Display the set of states
    3 |Display the set of input symbols (alphabet)
    4 |Display the set of final states
    5 |Display all transitions
    6 |Construct the equivalent regular grammar
      |Any other key to exit
        '''
        sys.exit(0) 

    print 'Processing option', option, '...'
    l = Logic()
    try:
        while option < 7:
            switch = {
                1: l.fromfile,
                2: l.showstates,
                3: l.showsymbols,
                4: l.showfinalstates,
                5: l.showtransitions,
                6: l.buildgrammar
            }[option]()
            print 'Choose another option:'
            option = int(sys.stdin.readline())
    except:
        print 'Unknown option.'
        sys.exit(0)
    
    print 'Exiting...'
    sys.exit(0) 

if __name__ == "__main__":
    main()
