#!/bin/python

import argparse
import csbgnpy.pd.utils
import sbgn2an.stories

usage = "usage: %stories.py INPUT"
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument("input", help="INPUT FILE")

args = parser.parse_args()

net = csbgnpy.pd.read_sbgnml(args.input)
stories = sbgn2an.stories.get_maximal_stories(net)
for i, ls in enumerate(stories):
    story = ls[1]
    label = ls[0]
    print("STORY {0} ({1})".format(i, label))
    print("{0}".format(','.join(story)))
