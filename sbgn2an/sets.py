import networkx

try:
    import clingo as gringo
    gringo_v = 5
except:
    import gringo
    gringo_v = 4

import sbgn2an.config

class StorySet(frozenset):
    def __str__(self):
        return "{{{}}}".format(','.join([str(story) for story in list(self)]))

class SetsControl(object):
    def __init__(self, net, stories):
        self.net = net
        self.stories = list(stories)
        self.selected = set()
        self.incompats = set()
        self._initialize_incompats()

    def reset(self):
        self.selected = set()
        self._initialize_incompats()

    def select(self, story):
        self.selected.add(story)
        self._update_incompats(story)

    def select_input(self, i):
        self.select(self.stories[i])

    def get_selection_candidates(self):
        candidates = set()
        for incompat in self.incompats:
            candidates = candidates.union(incompat)
        return candidates

    def _initialize_incompats(self):
        self.incompats = set()
        lincompats = []
        def _parse_model(model):
            incompats = set()
            if gringo_v == 4:
                atoms = [str(atom) for atom in model.atoms()]
            else:
                atoms = [str(atom) for atom in model.symbols(atoms = True)]
            for atom in atoms:
                if atom.startswith("incompat"):
                    l = atom[9:-1].split(',')
                    incompats.add((self.stories[int(l[0])], self.stories[int(l[1])]))
            return incompats
        def _on_model(model):
            lincompats.append(_parse_model(model))
        net_asp = sbgn2an.utils.cg2asp(self.net)
        stories_asp = sbgn2an.utils.stories2asp(self.stories)
        ctrl = gringo.Control()
        ctrl.load(sbgn2an.config.SETS_FILE)
        for rule in net_asp:
            ctrl.add("base", [], rule)
        for rule in stories_asp:
            ctrl.add("base", [], rule)
        ctrl.ground([("base", [])])
        res = ctrl.solve(on_model = _on_model)
        incompats = lincompats[0]
        g = networkx.Graph()
        for incompat in incompats:
            g.add_edge(incompat[0], incompat[1])
        cliques = networkx.find_cliques(g)
        for clique in cliques:
            self.incompats.add(frozenset(clique))

    def _update_incompats(self, selected):
        incompats = set()
        toremove = set()
        for incompat in self.incompats:
            if selected in incompat:
                toremove = toremove.union(incompat)
            else:
                incompats.add(incompat)
        self.incompats = set([incompat.difference(toremove) for incompat in incompats])

    def show_incompats(self):
        for incompat in self.incompats:
            print("{} : {}".format(" | ".join(["STORY {}".format(self.stories.index(story)) for story in incompat]), " | ".join([str(story) for story in incompat])))

    def solve(self, on_set = None, only_max = False, n = 0):
        net_asp = sbgn2an.utils.cg2asp(self.net)
        stories_asp = sbgn2an.utils.stories2asp(self.stories)
        ctrl = gringo.Control()
        ctrl.configuration.solve.models = n
        ctrl.load(sbgn2an.config.SETS_FILE)
        for rule in net_asp:
            ctrl.add("base", [], rule)
        for rule in stories_asp:
            ctrl.add("base", [], rule)
        for story in self.selected:
            ctrl.add("base", [], "inSet({}).".format(self.stories.index(story)))
        ctrl.ground([("base", [])])
        ctrl.ground([("sets", [])])
        if only_max:
            ctrl.ground([("max_incl", [])])
        self.on_set = on_set
        res = ctrl.solve(on_model = self._on_model)

    def _on_model(self, model):
        if self.on_set:
            s = self._parse_model(model)
            if s is not None:
                self.on_set(s)

    def _parse_model(self, model):
        s = []
        if gringo_v == 4:
            atoms = [str(atom) for atom in model.atoms()]
        else:
            atoms = [str(atom) for atom in model.symbols(atoms = True)]
        for atom in atoms:
            if atom.startswith("inSet"):
                sid = int(atom[:-1].split('(')[1])
                story = self.stories[sid]
                s.append(story)
        s = StorySet(s)
        return s
