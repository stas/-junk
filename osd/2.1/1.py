#!/usr/bin/env python

import commands
import yaml

DOCUMENT='users.yaml'

f = open(DOCUMENT)
data = yaml.load( f )
f.close()

for u in data:
    logins = commands.getoutput('last ' + u + ' | wc -l')
    data[u] = logins

f = open(DOCUMENT, "w")
yaml.dump( data, f )
f.close()

