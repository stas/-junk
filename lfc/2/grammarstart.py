#!/usr/bin/env python

import sys
from grammar.logic import Logic
from automata.logic import AutomataLogic

def main():
    option = None
    
    if len(sys.argv) > 1:
        option = int(sys.argv[1])
    else:
        print 'Usage: ', sys.argv[0], '<option ID>'
        print '''
    ID|Option description
    -----------------------
    1 |Read grammar from file
    2 |Display the set of nonterminal symbols
    3 |Display the set of terminal symbols
    4 |Display all the productions
    5 |Display the productions for a given nonterminal
    6 |Verify if grammar is correct
    7 |Construct automata
      |Any other key to exit
        '''
        sys.exit(0) 

    print 'Processing option', option, '...'
    l = Logic()
    l.automata = AutomataLogic()
    try:
        while option < 8:
            switch = {
                1: l.fromfile,
                2: l.show_nonterminals,
                3: l.show_terminals,
                4: l.show_productions,
                5: l.show_productsnonterm,
                6: l.verify_grammar,
                7: l.build_automata,
            }[option]()
            print 'Choose another option:'
            option = int(sys.stdin.readline())
    except:
        print 'Unknown option:', option
        sys.exit(0)
    
    print 'Exiting...'
    sys.exit(0) 

if __name__ == "__main__":
    main()
