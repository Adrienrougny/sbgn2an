#!/bin/python

import argparse
import csbgnpy.pd
import sbgn2an.utils

usage = "usage: %asp.py INPUT"
parser = argparse.ArgumentParser(usage = usage)
parser.add_argument("input", help="INPUT FILE")

args = parser.parse_args()

net = csbgnpy.pd.utils.read_sbgnml(args.input)
asp = sbgn2an.utils.cg2asp(net)
for rule in asp:
    print(rule)
