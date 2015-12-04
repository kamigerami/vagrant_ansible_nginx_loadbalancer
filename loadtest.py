#!/usr/bin/env python
#
# By Kami Gerami
# Load Testing Script
#
import httplib, argparse
from threading import Thread

def get_args():
    parser = argparse.ArgumentParser(description='Script runs threaded requests against given server n number of times')
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


def main():
    for i in range(threads):
        agent = Agent()
        agent.start()

class Agent(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(runtime):
            conn = httplib.HTTPConnection(host)
            conn.request('HEAD', "/")
            print conn.getresponse().getheader("X-Served-By")

if __name__ == '__main__':
    main()
