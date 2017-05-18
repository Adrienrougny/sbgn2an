#!/bin/python

import argparse
import csbgnpy.pd
import sbgn2an.utils

usage = "usage: %seeds.py INPUT"
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument("input", help="INPUT FILE")

args = parser.parse_args()

net = csbgnpy.pd.utils.read_sbgnml(args.input)
seeds = sbgn2an.utils.get_seeds(net)
for i, seed in enumerate(seeds):
    print("SEED {0}".format(i))
    print("{0}".format(','.join(seed)))
