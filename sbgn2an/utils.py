import networkx
# Backward compatibility with gringo 4.x
try:
    import clingo as gringo
    gringo_v = 5
except:
    import gringo
    gringo_v = 4

import sbgn2an.config
import csbgnpy.pd

def _quote_string(s):
    return '"{0}"'.format(s)

def cg2asp(net, empty_sets = False):
    l = []
    for entity in net.entities:
        if not isinstance(entity, csbgnpy.pd.entity.EmptySet):
            l.append("epn({0}).".format(entity.id))
            if hasattr(entity, "label"):
                l.append("labeled({0}, {1}).".format(entity.id, _quote_string(entity.label)))
            if hasattr(entity, "components"):
                for subentity in entity.components:
                    if hasattr(subentity, "label"):
                        l.append("labeled({0}, {1}).".format(entity.id, _quote_string(subentity.label)))
    for process in net.processes:
        reactants = process.reactants
        products = process.products
        for reactant in reactants:
                for product in products:
                    if not empty_sets:
                        if not isinstance(reactant, csbgnpy.pd.entity.EmptySet) and not isinstance(product, csbgnpy.pd.entity.EmptySet):
                            l.append("edge({0},{1},{2}).".format(reactant.id, product.id, process.id))
                    else:
                            l.append("edge({0},{1},{2}).".format(reactant.id, product.id, process.id))
    return l

def get_sccs(net):
    g = networkx.DiGraph()
    for process in net.processes:
        for reactant in set(process.reactants):
            g.add_edge(reactant, process)
        for product in set(process.products):
            g.add_edge(process, product)
    sccs = networkx.strongly_connected_components(g)
    return sccs

def get_sources(net):
    sources = set()
    for e in net.entities:
        issource = True
        for process in net.processes:
            if e in process.products:
                issource = False
                break
        if issource:
            sources.add(e)
    return sources

def stories2asp(stories):
    l = []
    for i, story in enumerate(stories):
        l.append("story({}).".format(i))
        for e in story:
            l.append("inStory({},{}).".format(e.id, i))
    return l

class SeedsControl(object):
    def __init__(self, net, n = 0):
        self.net = net

    def solve(self, on_seed = None, n = 0):
        asp = sbgn2an.utils.cg2asp(self.net, empty_sets = True)
        ctrl = gringo.Control()
        ctrl.configuration.solve.models = n
        ctrl.load(sbgn2an.config.SEEDS_FILE)
        for rule in asp:
            ctrl.add("base", [], rule)
        ctrl.ground([("base", [])])
        self.on_seed = on_seed
        res = ctrl.solve(on_model = self._on_model)

    def _on_model(self, model):
        if self.on_seed:
            seed = self._parse_model(model)
            self.on_seed(seed)

    def _parse_model(self, model):
        seed = []
        if gringo_v == 4:
            lits = [str(lit) for lit in model.atoms()]
        else:
            lits = [str(lit) for lit in model.symbols(atoms = True)]
        for lit in lits:
            if lit.startswith("seed"):
                seed.append(lit[:-1].split('(')[1])
        return seed

def get_seeds(net, n = 0):
    seeds = []
    def on_seed(seed):
        seeds.append(seed)
    ctrl = SeedsControl(net)
    ctrl.solve(on_seed, n)
    return seeds
