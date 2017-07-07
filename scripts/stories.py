#!/bin/python
import sbgn2an.utils


import time
import argparse
import csbgnpy.pd.sbgnmlio
import sbgn2an.stories

usage = "usage: %stories.py INPUT"
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument("--same-labels", action = "store_true", default = False)
parser.add_argument("--only-max", action = "store_true", default = False)
parser.add_argument("-n", default = 0)
parser.add_argument("input", help="INPUT FILE")

args = parser.parse_args()

opts = vars(args)

print("######################################################################################")
print("ARGUMENTS")
for key in opts.keys():
    print("{}: {}".format(key, opts[key]))
print("######################################################################################")

start = time.time()
net = csbgnpy.pd.sbgnmlio.read_sbgnml(args.input)
end = time.time()
print("Read file in {} seconds".format(end-start))
start = time.time()
stories = sbgn2an.stories.get_stories(net, args.same_labels, args.only_max, args.n)
end = time.time()
print("Enumerated all stories in {} seconds".format(end-start))
for i, story in enumerate(stories):
    print("STORY {}".format(i))
    print(story)
