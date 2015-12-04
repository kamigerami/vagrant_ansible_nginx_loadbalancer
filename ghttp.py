#!/usr/bin/env python
import httplib
import argparse


parser = argparse.ArgumentParser(description="Get http Response from Webserver")
parser.add_argument("-i", "--ip", dest="host", help="ip address of the loadbalancer")
parser.add_argument("-n", "--num", dest="times", type=int, help="number of times to run")

args = parser.parse_args()

def get_http_response(host, times):

    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", "/")
        return conn.getresponse().reason
    except StandardError:
        return None

print get_http_response(args.host, args.times)
