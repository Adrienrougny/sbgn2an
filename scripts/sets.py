#!/bin/python

import argparse
import csbgnpy.pd
import sbgn2an.stories

usage = "usage: %sets.py INPUT"
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument("input", help="INPUT FILE")
parser.add_argument("--story", action="append")

args = parser.parse_args()

stories = None
if args.story is not None:
    stories = [s.split(",") for s in args.story]

net = csbgnpy.pd.utils.read_sbgnml(args.input)
sets = sbgn2an.stories.get_sets_of_stories(net, stories)
for i, sset in enumerate(sets):
    print("SET {0} ({1})".format(i, sum([len(story) for story in sset])))
    for j, story in enumerate(sset):
        print("STORY {0}".format(j))
        print("{0}".format(','.join(story)))
