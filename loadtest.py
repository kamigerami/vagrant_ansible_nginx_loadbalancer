#!/usr/bin/env python
#
# By Kami Gerami
# Load Testing Script
#
import httplib, argparse
from threading import Thread
from collections import defaultdict # requires python 2.7

def get_args():
    parser = argparse.ArgumentParser(description='Script runs x threaded requests against given server n number of times')
    # argument options
    parser.add_argument(
        '-s', '--server', help='Server name or Ip', required=True)
    parser.add_argument(
        '-n', '--number', type=int, help='Number of iterations to run (default=5)', required=False, default=5)
    parser.add_argument(
        '-t', '--thread', type=int, help='Thread count (default=2)', required=False, default=2)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assigning args to variables
    host = args.server
    runtime = args.number
    threads = args.thread
    # Return all variable values
    return host, runtime, threads

# getting arguments
get_args()
# Matching return values from get_args()
# and assigning to their respective variables
host, runtime, threads = get_args()


thread_count = 0

def main():

    for i in range(threads):
        agent = Agent()
        agent.start()

class Agent(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global thread_count
        counter = defaultdict(int)
        server_hit_count = []
        for i in range(runtime):
            conn = httplib.HTTPConnection(host)
            conn.request('GET', "/", headers={'cache-control':'no-cache'})
            resp_host = conn.getresponse().read()
            server_hit_count.append(resp_host)
        for hosts in server_hit_count:
            counter[hosts] += 1
        thread_count += 1
        for srv, cnt in counter.iteritems():
            print "Thread nr: %d" %(thread_count)
            print "%s" %(srv.rstrip())
            print "Hit counter: %d" %(cnt)
            print ""

if __name__ == '__main__':
    main()
