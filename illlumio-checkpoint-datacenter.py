#!/usr/bin/env python3

import os
from illumio import *
import argparse
import json

# Initialize the parser
parser = argparse.ArgumentParser(description='Process some inputs')

# Add arguments
parser.add_argument('--pce_host', required=True, help='PCE Host')
parser.add_argument('--pce_port', help='PCE Port', default=443)
parser.add_argument('--pce_org', help='PCE Org', default=1)
parser.add_argument('--pce_api_user', required=True, help='PCE API User')
parser.add_argument('--pce_api_secret', required=True, help='PCE API Secret')
parser.add_argument('--labels', type=lambda s: [item for item in s.split(',')], help='Comma-separated list of labels to retrieve', default=['role', 'app', 'env', 'loc'])
parser.add_argument('--limit', type=int, default=500, help='Count limit of workloads to retrieve (default: 500)')
parser.add_argument('--output', help='Output file', default='illumio-checkpoint.json')

# Parse the arguments
args = parser.parse_args()
print(args.labels)

pce = PolicyComputeEngine(args.pce_host, port=args.pce_port, org_id=args.pce_org)
pce.set_credentials(args.pce_api_user, args.pce_api_secret)

if pce.check_connection():
    print("Successfully connected to the PCE")
else:
    print("Failed to connect to the PCE")
    exit()


# checkpoint header: https://support.checkpoint.com/results/sk/sk167210
# initial json data
checkpoint = {
    "version": "1.0",
    "description": "Illumio Workload export example",
    "objects": []
}

# two dicts for caching the label hrefs
label_href_map = {}
value_href_map = {}

# fill label dict, this reads all labels and puts the object into a value of a dict. The dict key is the label name.
for l in pce.labels.get():
    label_href_map[l.href] = { "key": l.key, "value": l.value }
    value_href_map["{}-{}".format(l.key, l.value)] = l.href

workloads = pce.workloads.get()
count_wl = len(workloads)
print("Retrieved {} workloads".format(count_wl))

for workload in workloads:
    uuid = os.path.basename(workload.href)

    labels_as_string = ''
    
    for l in workload.labels:
        label = label_href_map[l.href]
        key = label['key'].replace(" ", "_")
        value = label['value'].replace(" ", "_")
        labels_as_string = labels_as_string + "|{}={}".format(key, value)

    ### initialize the workload dict
    wldict = {}
    name = workload.hostname if workload.hostname is not None else workload.name

    wldict['name'] = "{} {}".format(name, labels_as_string) 
    wldict['id'] = uuid
    wldict['description'] = 'Illumio export'
    wldict['ranges'] = []
    
    
    for iface in workload.interfaces:
        wldict['ranges'].append(iface.address)
        
    checkpoint['objects'].append(wldict)
    
if args.output:
    with open(args.output, 'w') as outfile:
        json.dump(checkpoint, outfile, indent=4)
        print("Wrote output file: {}".format(args.output))
else:
    print(json.dumps(checkpoint, indent=4))
