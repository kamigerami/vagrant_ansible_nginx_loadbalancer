#!/usr/bin/env python
#
# By Kami Gerami
# Load Testing Script
#
import httplib, argparse
from collections import defaultdict # requires python 2.7

def get_args():
    parser = argparse.ArgumentParser(description='Script runs requests against given server n number of times')
    # argument options
    parser.add_argument(
        '-s', '--server', help='Server name or Ip', required=True)
    parser.add_argument(
        '-n', '--number', type=int, help='Number of iterations to run (default=5)', required=False, default=5)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assigning args to variables
    host = args.server
    runtime = args.number
    # Return all variable values
    return host, runtime

# getting arguments
get_args()
# Matching return values from get_args()
# and assigning to their respective variables
host, runtime = get_args()


def main():

        counter = defaultdict(int)
        server_hit_count = []
        for i in range(runtime):
            conn = httplib.HTTPConnection(host)
            conn.request('GET', "/", headers={'cache-control':'no-cache'})
            resp_host = conn.getresponse().read()
            server_hit_count.append(resp_host)
        for hosts in server_hit_count:
            counter[hosts] += 1
        for srv, cnt in counter.iteritems():
            print "%s" %(srv.rstrip())
            print "Hit counter: %d" %(cnt)
            print ""

if __name__ == '__main__':
    main()
