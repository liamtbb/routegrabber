#!/usr/bin/env python

import os, logging, sys, time, argparse, ast, telnetlib, whois
from func import telnet_connect, find_as_path, scrape_asn, resolve_asn, scrape_collectors, load_asn



## logging setup
# create logger with 'network_backups'
logger = logging.getLogger('routegrabber.log')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
# fh = logging.FileHandler(log_dir)
# fh.setLevel(logging.DEBUG)

# create console handler with it's own log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)



## argument parsing
parser = argparse.ArgumentParser(description = "Options for routegrabber")
parser.add_argument("-v", "--verbose", help = "Enables verbose output", action="store_true")
parser.add_argument("-u", "--update", help = "Creates or updates ASN cache file asn_cache.txt", action="store_true")
parser.add_argument("-a", "--asn", help = "Returns organization description for ASN value", action="store", dest="asn")
parser.add_argument("-d", "--descriptions", help = "Resolves ASN paths to organization descriptions", action="store_true")
parser.add_argument("-r", "--route", help = "set route for AS path query", action="store", dest="route")

args = parser.parse_args()

if args.update:
    scrape_asn()
    print("asn cache has been updated.")
    exit()

if args.route is not None:
    route = args.route
else:
    print("No route set, please include with '-r <route>' argument.\n")
    exit()



## directory management
# date = str(date.today())
#last_date = date.today() - timedelta(days=1)
#root_dir = "/usr/home/astutebackups/backups/network_backups/"
#save_dir = os.path.join(root_dir, str(date))
#log_dir = (root_dir + "network_backups_" + str(date) + ".log")
#last_log_dir = (root_dir + "network_backups_" + str(last_date) + ".log")

#if not os.path.exists(save_dir):
#    os.mkdir(save_dir)



## gather whois data
# w = whois.whois(route)
# print("Gathering route information for " + route + "\n")
# print(w)
# exit()



## telnet actions
host = "route-views3.routeviews.org"
# host = "route-views.ny.routeviews.org"
# route = "199.167.19.119"
command1 = "show bgp summary"
command2 = "show ip bgp " + route



## retrieve route information
telnetOutput = telnet_connect(host, command1, command2)



## parse for as path info
asPathOutput = find_as_path(telnetOutput)



## load asn_cache.txt to asnDict
asnDict = load_asn()



## retrieve collector list from web
# collectorList = scrape_collectors
# print(collectorList)



## resolve ASNs to organization description
asPathResolved = resolve_asn(asnDict, asPathOutput)



## print AS paths
c = 0
print("AS paths to " + route + ":\n")
asPathNatural = []
for i in asPathOutput:
    c = c + 1
    asPathNatural = (' '.join(i))
    print("Route " + str(c) + ": " + asPathNatural)



## print resolved AS paths with separator element (if descriptions option selected)
if args.descriptions:
    c = 0
    print("\n\nResolved AS path IDs:\n")
    asPathJoined = []
    for i in asPathResolved:
        c = c + 1
        asPathJoined = (' <-->'.join(i))
        print("Route " + str(c) + ": " + asPathJoined)



exit()