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
parser.add_argument("-o", default = "stdout")
parser.add_argument("input", help="INPUT FILE")

args = parser.parse_args()

opts = vars(args)

print("######################################################################################")
print("ARGUMENTS")
for key in opts.keys():
    if key != "o":
        print("{}: {}".format(key, opts[key]))
    else:
        print("output: {}".format(opts[key]))
print("######################################################################################")
print("Building network from file...")
start = time.time()
net = csbgnpy.pd.sbgnmlio.read_sbgnml(args.input)
end = time.time()
print("Built network in {} seconds".format(end-start))
print("Enumerating stories...")
start = time.time()
stories = sbgn2an.stories.get_stories(net, args.same_labels, args.only_max, args.n)
end = time.time()
print("Enumerated {} stories in {} seconds".format(len(stories), end-start))
s = ""
for i, story in enumerate(stories):
    labels = story.get_labels()
    if len(labels) == 0:
        s += "STORY {}\n".format(i+1)
    else:
        s += "STORY {} ({})\n".format(i+1, ','.join(labels))
    s += "{}\n".format(story)
if args.o == "stdout":
    print(s)
else:
    f = open(args.o, 'w')
    f.write(s)
    f.close()
