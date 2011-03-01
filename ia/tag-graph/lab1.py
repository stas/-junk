from pprint import pformat

class TadGraph:
    g = None
    matrix = None
    nodes = []
    
    def read(self, filename):
        f = file(filename)
        matrix = []
        
        for line in f:
            line = line.strip()
            if( len(line) ) == 0:
                continue
            
            row = line.split(',')
            matrix.append( row )
        
        f.close()
        self.matrix = matrix
    
    def write(self, filename):
        of = open(filename, "w")
        of.write( pformat(self.g) )
        of.write( "\n" )
        of.close()
    
    def graph(self, data):
        current = 1
        nodes = {}
        for e in data:
            v = []
            vindex = 1
            for i in e:
                if int(i) > 0:
                    v.append(vindex)
                vindex +=1
            nodes[current] = v
            current += 1
        self.g = nodes
    
    def output(self):
        for e in self.g:
            print str(e) + " "
            for i in self.g[e]:
                print "->" + str(i),
            print "\n"
    
    def connected(self, source, target ):
        if source in self.g.keys() and target in self.g.keys():
            if target in self.g[source]:
                return True
            else:
                return False
        else:
            return "Not a node!"
    
    def path(self, start, end):
        found = False
        if start in self.g.keys() and end in self.g.keys():
            #verts = None
            #for v in self.g:
            return "Not implemented"
        else:
            return "Not a node!"
