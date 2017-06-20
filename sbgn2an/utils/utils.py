
# Backward compatibility with gringo 4.x
try:
    import clingo
except:
    import gringo

import sbgn2an.config
import csbgnpy.pd

def _quote_string(s):
    return '"{0}"'.format(s)

def cg2asp(net):
    l = []
    for entity in net.entities:
        if not isinstance(entity, csbgnpy.pd.EmptySet):
            l.append("epn({0}).".format(entity.id))
            if entity.has_label():
                l.append("labeled({0}, {1}).".format(entity.id, _quote_string(entity.label)))
            for subentity in entity.components:
                if subentity.has_label():
                    l.append("labeled({0}, {1}).".format(entity.id, _quote_string(subentity.label)))
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
                    if not isinstance(reactant, csbgnpy.pd.EmptySet) and not isinstance(product, csbgnpy.pd.EmptySet):
                    # if not net.isSink(product):
                        l.append("edge({0},{1},{2}).".format(reactant.id, product.id, process.id))
    return l

class SeedsControl(object):
    def __init__(self, net, n = 0):
        self.net = net
        self.conf = n
        self.asp = sbgn2an.utils.cg2asp(net)
        self.ctrl = gringo.Control()
        self.ctrl.conf.solve.models = self.conf
        self.ctrl.load(sbgn2an.config.SEEDS_FILE)
        for rule in self.asp:
            self.ctrl.add("base", [], rule)
        self.ctrl.ground([("base", [])])

    def solve(self, on_seed = None):
        self.on_seed = on_seed
        res = self.ctrl.solve(on_model = self._on_model)

    def _on_model(self, model):
        if self.on_seed is not None:
            seed = self._parse_model(model)
            self.on_seed(seed)

    def _parse_model(self, model):
        seed = []
        for lit in [str(lit) for lit in model.atoms()]:
            if lit.startswith("seed"):
                seed.append(lit[:-1].split('(')[1])
        return seed

def get_seeds(net, n = 0):
    seeds = []
    def on_seed(seed):
        seeds.append(seed)
    ctrl = SeedsControl(net)
    ctrl.solve(on_seed = on_seed)
    return seeds
