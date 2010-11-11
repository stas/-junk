#!/usr/bin/env python
import signal
import os
import time
import sys

def kirks_log(signum, stack):
    logpath = "/tmp/kirk.log"
    if( os.path.exists(logpath) ):
        f = open(logpath)
        print f.read()
        f.close()
        os.remove(logpath)
    else:
        print "No log found"

def spock_to_enterprise():
    e_pidfile = "/tmp/enterprise.py.pid"
    while True:
        if( os.path.exists(e_pidfile) ):
            f = open( e_pidfile )
            e_pid = f.readline()
            f.close()
            print "Spock, enterprise is at:", e_pid, ", sending signal..."
            os.kill(int(e_pid), signal.SIGUSR1)
            time.sleep(30)
        else:
            print "Spock, enterprise is down"
            time.sleep(30)
    
    sys.exit(0)

def main():
    pidfile = "/tmp/spock.py.pid"
    if( os.path.exists(pidfile) ):
        print "Spock didn't die yet. Exiting..."
        sys.exit(1)
    else:
        f = open(pidfile, "w")
        our_pid = os.getpid()
        f.write(repr(our_pid))
        f.close()
    
    signal.signal(signal.SIGUSR1, kirks_log)
    spock_to_enterprise()
    os.remove(pidfile)
    sys.exit(0)

if __name__ == "__main__":
    main()
