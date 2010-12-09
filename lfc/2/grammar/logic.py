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
        self.states = line.split(' ')

        if len(self.nonterminals) < 1:
            print 'Error at line 1: The set of nonterminals expected'
            self.nonterminals = None
        else:
            print 'Non terminal symbols:'
            print self.nonterminals

        return

    def show_terminals(self):
        line = self.filelines[1].strip()
        self.states = line.split(' ')

        if len(self.terminals) < 1:
            print 'Error at line 1: The set of terminals expected'
            self.terminals = None
        else:
            print 'Terminal symbols:'
            print self.terminals


        # Starting symbol
        line = self.filelines[2].strip()
        self.startsymbol = line.split(' ')
        
        if len(self.startsymbol) < 1:
            print 'Error at line 3: The start symbol expected'
            self.startsymbol = None
        else:
            print 'Start symbol:'
            print self.startsymbol

        return

    def show_productions(self):
        line = self.filelines[3].strip()
        self.productions = {}
        production = line.split(' ')

        if len(self.productions) is not 2:
            print 'Error at line 1: The set of productions expected'
            self.terminals = None
        else:
            self.productions[production[0]] = production[1]
            print 'Productions:'
            print self.productions
        return

    def show_productsnonterm(self):
        for n in self.nonterminals:
            print get_products(n)

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

    def verify_grammar(self):
        exists = False
        prods = self.get_products(self.startsymbol)
        if prods and 'e' in prods:
            exists = True

        for n in self.nonterminals:
            for p in prods:
                if len(p) is 1:
                    if p in self.terminals:
                        return False
                    else:
                        if n is not self.startsymbol:
                            return False
                if len(p) is 2:
                    if p[0] in self.terminals or p[1] in self.nonterminals:
                        return False
                    if exists:
                        if p[1] is self.startsymbol:
                            return False
        return True

    def build_automata(self):
        return

    def get_products(self, nonterminal):
        if nonterminal in self.nonterminals:
            if nonterminal in self.productions.keys():
                return self.productions[nonterminal]
        else:
            return None
