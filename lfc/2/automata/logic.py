#!/usr/bin/env python

import sys
import os

from string import join
from grammar import Grammar

class Logic:
    filepath = None
    filedata = None
    filelines = None
    states = None
    initialstate = None
    symbols = None
    finalstates = None
    transitions = None
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
        
    def showstates(self):
        line = self.filelines[0].strip()
        self.states = line.split(' ')
        
        if len(self.states) < 1:
            print 'Error at line 1: The set of states expected'
            self.states = None
        else:
            print 'States:'
            print self.states
        
        # Initial states
        line = self.filelines[2].strip()
        self.initialstate = line.split(' ')
        
        if len(self.initialstate) > 2:
            print 'Error at line 3: The initial states expected'
            self.initialstate = None
        else:
            print 'Initial states:'
            print self.initialstate
        
        return

    def showsymbols(self):
        line = self.filelines[1].strip()
        self.symbols = line.split(' ')
        
        if len(self.symbols) < 1:
            print 'Error at line 2: The set of symbols expected'
            self.symbols = None
        else:
            print 'Symbols:'
            print self.symbols
        
        return

    def showfinalstates(self):
        line = self.filelines[3].strip()
        self.finalstates = line.split(' ')
        
        if len(self.finalstates) < 1:
            print 'Error at line 2: The set of final states expected'
            self.finalstates = None
        else:
            print 'Final states:'
            print self.finalstates
            
        return

    def showtransitions(self):
        lines = self.filelines[4:]
        l_nr = 4

        for l in lines:
            l_nr+=1
            l = l.strip()
            if l:
                l = l.split(' ')
        
            if len(l) is not 3:
                print 'Error at line', l_nr, ': A transition function expected'
            elif self.transitions is None:
                self.transitions = list()
                self.transitions.append(l)
            else:
                self.transitions.append(l)
        
        if len(self.transitions) < 1:
            self.transitions = None
            print 'Error: Some transition functions expected' 
        else:
            print 'Transitions:'
            for t in self.transitions:
                print "delta(%s, %s) = %s" % (t[0], t[1], t[2])
        
        return

    def buildgrammar(self):
        g = Grammar()
        g.nonterminals = self.states
        g.terminals = self.symbols
        g.startsymbol = str(self.initialstate)
        
        tf = self.transitions
        if len(tf) > 0:
            for t in tf:
                if len(t) == 3:
                    g.add_production(t[0], t[1] + t[2])
                    if t[2] in self.finalstates:
                        g.add_production(t[0], t[1] + '')
        
        if g.starsymbol in self.finalstates:
            g.add_production(g.starsymbol, 'e')
        
        self.grammar = g

        print 'Nonterminals: ', self.grammar.nonterminals
        print 'Terminals: ', self.grammar.terminals
        print 'Start symbol: ', self.grammar.startsymbol
        print 'Productions: ', self.grammar.productions

        return
