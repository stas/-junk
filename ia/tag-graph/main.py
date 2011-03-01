from lab1 import TadGraph
from pprint import pprint

g = TadGraph()
g.read( 'matrix.text' )
#pprint(g.matrix)
g.graph( g.matrix )
pprint( g.g )
#g.output()
print g.connected( 1, 2 )
print g.path( 1, 4 )
#g.write( 'new_matrix.text' )

