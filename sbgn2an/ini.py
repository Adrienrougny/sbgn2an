import os

import clingo

import csbgnpy.pd.io.sbgnml
import sbgn2an.stories
import sbgn2an.config

def get_ini(net, in_ini = None, stories = None):
    ctrl = clingo.Control(["--warn=none", "-n 0", "--opt-mode=optN"])
    # ctrl = clingo.Control(["--warn=none", "-n 0"])
    # ctrl = clingo.Control(["-n 0"])
    ctrl.load(sbgn2an.config.INI_FILE)
    atoms = sbgn2an.utils.cg2asp(net, empty_sets = True)
    for atom in atoms:
        ctrl.add("base", [], atom)
    if in_ini:
        for e in in_ini:
            ctrl.add("base", [], "inIni({}).".format(e.id))
    if stories:
        for i, story in enumerate(stories):
            for e in story:
                ctrl.add("base", [], "inStory({},{}).".format(e.id, i))
    ctrl.ground([("base", [])])

    models = []

    def on_model(model):
        if model.optimality_proven:
            models.append([net.get_entity(str(atom).split('(')[1][:-1], by_id = True) for atom in model.symbols(shown=True)])

    ctrl.solve(on_model = on_model)
    return models
