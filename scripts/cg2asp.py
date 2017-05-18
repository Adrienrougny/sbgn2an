#!/bin/python
import argparse
import csbgnpy.PD

def quote_string(s):
    return '"{0}"'.format(s)

def cg2asp(net):
    l = []
    for entity in net.entities:
        if not isinstance(entity, csbgnpy.PD.EmptySet):
            l.append("epn({0}).\n".format(entity.id))
            if entity.has_label():
                l.append("labeled({0}, {1}).\n".format(quote_string(entity.label), entity.id))
                for subentity in entity.components:
                    if subentity.has_label():
                        l.append("labeled({0}, {1}).\n".format(quote_string(subentity.label), entity.id))
    for process in net.processes:
        reactants = process.reactants
        products = process.products
        # if len(reactants) == 0:
        #     for product in products:
        #         for product2 in products:
        #             if product != product2:
        #                 s += "edge({0},{1},{2}).\n".format(product.id, product2.id, process.id)
        # else:
        for reactant in reactants:
                for product in products:
                    if not isinstance(reactant, csbgnpy.PD.EmptySet) and not isinstance(product, csbgnpy.PD.EmptySet):
                    # if not net.isSink(product):
                        l.append("edge({0},{1},{2}).\n".format(reactant.id, product.id, process.id))
    return s

usage = "usage: %sbgnpd2asp.py FILES"
parser = argparse.ArgumentParser()
parser.add_argument("input", action = "append")
parser.add_argument("-o")
args = parser.parse_args()
filenames = args.input

net = csbgnpy.PD.Utils.read_SBGNML(*filenames)
l = cg2asp(net)
s = "\n".join(l)

if args.o:
    f = open(args.o, 'w')
    f.write(s)
    f.close()
else:
    print(s)
