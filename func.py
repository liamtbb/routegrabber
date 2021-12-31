import os, logging, sys, time, argparse, ast, telnetlib, re, requests, itertools, json
from itertools import chain

# from requests.sessions import RecentlyUsedContainer



def telnet_connect(host, command1, command2):

    print("Connecting to " + host + ".")

    tn = telnetlib.Telnet(host)
    tn.write(b"\n")

    print("Connected to " + host + ".\n")

    tn.write(command1.encode('ascii') + b"\r") ### run command1
    tn.write(command2.encode('ascii') + b"\r") ### run command2
    # tn.write(command3.encode('ascii') + b"\r") ### run command3
    time.sleep(3)
    tn.write(b"exit\r")

    print("Exiting from " + host + ".\nYou can see output from device below:\n")

    # print(tn.read_all().decode('ascii'))

    telnetOutput = tn.read_all().decode('ascii') ### add entire output to return value

    return telnetOutput


def find_as_path(telnetOutput):

    pattern = "(?:\n\s{2})(?:\d+\s{1}){1,}"

    asPaths = re.findall(pattern, telnetOutput)

    asPathsClean = []
    asPathsSplit = []

    for i in asPaths:
        asPathsClean.append(i.strip())

    for i in asPathsClean:
        asPathsSplit.append(i.split())

    return asPathsSplit


def scrape_asn():

    URL = "https://bgp.potaroo.net/cidr/autnums.html" ### site with all ASNs
    page = requests.get(URL)

    patternAsn = "(?<=\"\>AS)(\d{1,7})" ### pattern match for ASN
    patternDesc = "(?<=\<\/a>).*" ### pattern match for AS organization description

    asnList = re.findall(patternAsn, page.text)
    asnListDesc = re.findall(patternDesc, page.text)

    asnDict = {asnList[i]: asnListDesc[i] for i in range(len(asnList))}

    with open('asn_cache.txt', 'w') as file:
        file.write(json.dumps(asnDict))

    return asnDict


def load_asn():

    with open('asn_cache.txt') as json_file:
        asnDict = json.load(json_file)

    return asnDict


def scrape_collectors():

    URL = "http://www.routeviews.org/routeviews/index.php/collectors/" ### routeviews collectors page
    page = requests.get(URL)

    patternCollector = "(?<=\"\>AS)(\d{1,7})" ### pattern match for ASN

    # collectorList = re.findall(patternCollector, page.text)
    collectorList = page.text

    return collectorList



def resolve_asn(asnDict, asPathOutput):

    asPathResolved = [[asnDict[key] for key in key_set ] for key_set in asPathOutput]

    return asPathResolved