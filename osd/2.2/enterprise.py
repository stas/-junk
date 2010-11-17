#!/usr/bin/env python

import os
import signal
import sys
import time

def kirk_logs(signum, stack):
    logpath = "/tmp/kirk.log"
    print "Kirk, say something:"
    msg = sys.stdin.readline()
    f = open(logpath, "w")
    f.write(repr(msg))
    f.close()

def enterprise_to_spock():
    s_pidfile = "/tmp/spock.py.pid"
    while True:
        if( os.path.exists(s_pidfile) ):
            f = open( s_pidfile )
            s_pid = f.readline()
            f.close()
            print "Enterprise, spock is at:", s_pid, ", sending signal..."
            os.kill(int(s_pid), signal.SIGUSR1)
            time.sleep(10)
        else:
            print "Enterprise can't find spock..."
            time.sleep(10)
    
    sys.exit(0)

def main():
    pidfile = "/tmp/enterprise.py.pid"
    if( os.path.exists(pidfile) ):
        print "One USS is enough for our galaxy. Exiting..."
        sys.exit(1)
    else:
        f = open(pidfile, "w")
        our_pid = os.getpid()
        f.write(repr(our_pid))
        f.close()
    
    signal.signal(signal.SIGUSR1, kirk_logs)
    enterprise_to_spock()
    os.remove(pidfile)
    sys.exit(0)

if __name__ == "__main__":
    main()
