#!/usr/bin/env python

import sys
import os

class Grammar:
    nonterminals = None
    terminals = None
    productions = None
    starsymbol = None
    
    def add_production(self, lhs, rhs):
        for l in rhs:
            if l is not 'e':
                if l not in self.nonterminals and l not in self.terminals:
                    print "Error, could not find symbol:", l

        if not self.productions:
            self.productions = {}
        
        self.productions[lhs] = rhs
        
        return
