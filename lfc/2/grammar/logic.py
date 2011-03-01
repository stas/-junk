#!/usr/bin/env python

import sys
import os

from string import join

class Logic:
    filepath = None
    filedata = None
    filelines = None
    nonterminals = None
    terminals = None
    startsymbol = None
    productions = None
    grammar = None
    automata = None

    def fromfile(self):
        if self.filepath is None:
            print 'Write the filename:',
            fpath = sys.stdin.readline()
            self.filepath = fpath.rstrip()
        
        print 'Reading from:',self.filepath
        if os.path.isfile(self.filepath) and not self.filedata:
            file_h = open(self.filepath, "r")
            self.filedata = file_h.read()
            file_h.close()
        
        if self.filedata:
            print 'File data:'
            print '---'
            print self.filedata
            print '---'
        
        if self.filelines is None:
            self.filelines = self.filedata.split('\n')
        
        return

    def show_nonterminals(self):
        line = self.filelines[0].strip()
        self.nonterminals = line.split(' ')

        if len(self.nonterminals) < 1:
            print 'Error at line 1: The set of nonterminals expected'
            self.nonterminals = None
        else:
            print 'Non terminal symbols:'
            print self.nonterminals
        return

    def show_terminals(self):
        line = self.filelines[1].strip()
        self.terminals = line.split(' ')

        if len(self.terminals) < 1:
            print 'Error at line 1: The set of terminals expected'
            self.terminals = None
        else:
            print 'Terminal symbols:'
            print self.terminals


        # Starting symbol
        line = self.filelines[2].strip()
        self.startsymbol = line.split(' ')
        self.startsymbol = str(self.startsymbol[0])
        
        if len(self.startsymbol) < 1:
            print 'Error at line 3: The start symbol expected'
            self.startsymbol = None
        else:
            print 'Start symbol:'
            print self.startsymbol

        return

    def show_productions(self):
        self.productions = {}
        lines = self.filelines[3:]
        for line in lines:
            if line:
                line = line.strip()
                production = line.split(' ')
                production[1] = [str(c) for c in production[1]]
        
                if len(production) is not 2:
                    print 'Error at line 1: The set of productions expected'
                    self.terminals = None
                else:
                    if self.productions.has_key(production[0]):
                        self.productions[production[0]].append(production[1])
                    else:
                        self.productions[production[0]] = list()
                        self.productions[production[0]].append(production[1])
        
        print 'Productions:'
        print self.productions
        return

    def show_productsnonterm(self):
        print 'Type the non-terminal:',
        fpath = sys.stdin.readline()
        n = fpath.rstrip()
        print self.get_products(n)
        return

    def is_grammar(self):
        if not get_products(self.startsymbol):
            return False

        nr_nonterminals = len(self.nonterminals)
        index = 0
        for nn in self.nonterminals:
            if self.starsymbol is nn:
                nr_nonterminals[index] = -1
            else:
                nr_nonterminals[index] = 0
            index += 1

        for n_index in xrange(0, len(self.nonterminals)+1):
            prods = self.get_products(nn)
            for nn_index in xrange(0, len(self.nonterminals)+1):
                if n_index is not nn_index:
                    if nr_nonterminals[nn_index] is not -1:
                        if self.nonterminals[nn_index] in self.productions:
                            nr_nonterminals[nn_index] = nr_nonterminals[nn_index] + 1

        for n_index in xrange(0, len(self.nonterminals)+1):
            if nr_nonterminals[n_index] is 0:
                print 'A nonterminal does not appear in the right side of any production'
                return False

        return True

    def check_grammar(self):
        prods = self.productions.get(self.startsymbol)
        if prods:
            for p in prods:
                if 'e' in p:
                    exists = True
                    break
        
        for n in self.nonterminals:
            prods = self.get_products(n)
            for p in prods:
                if 'e' not in p: # Skip checks for 'e'
                    in_terminals = False
                    for p0 in p: # Check for terminals
                        for t in p0:
                            if t in self.terminals:
                                in_terminals = True
                                break
                    
                    if not in_terminals:
                        return False
                else:
                    if n is not self.startsymbol:
                        return False
        return True
    
    def verify_grammar(self):
        print self.check_grammar()
        return
    
    def build_automata(self):
        if not self.automata:
            return
        
        self.automata.states = self.nonterminals
        self.automata.states.append('K')
        self.automata.symbols = self.terminals
        self.automata.initialstate = self.startsymbol
        self.automata.finalstates.append('K')
        
        if 'e' in self.get_products(self.startsymbol):
            self.automata.finalstates.append(self.startsymbol)
        
        for nt in self.nonterminals:
            prods = self.get_products(nt)
            if prods:
                for p in prods:
                    if 'e' not in p:
                        
        
        return

    def get_products(self, nonterminal):
        if nonterminal in self.nonterminals:
            if nonterminal in self.productions.keys():
                return self.productions[nonterminal]
        else:
            return None
