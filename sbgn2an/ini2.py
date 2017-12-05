import os

import clingo

import csbgnpy.pd.io.sbgnml
import csbgnpy.pd.io.sbgnlog
import sbgn2an.stories
import sbgn2an.config

def get_ini(net, stories = None):
    # ctrl = clingo.Control(["--warn=none", "-n 0", "--opt-mode=opt"])
    ctrl = clingo.Control(["--warn=none", "-n 0"])
    # ctrl = clingo.Control(["-n 0"])
    ctrl.load(sbgn2an.config.INI_FILE)
    ctrl.load(sbgn2an.config.PD_ONTO_FILE)
    atoms = csbgnpy.pd.io.sbgnlog.network_to_atoms(net, use_ids = True)
    for atom in atoms:
        ctrl.add("base", [], str(atom) + '.')
    if stories:
        for i, story in enumerate(stories):
            for e in story:
                ctrl.add("base", [], "inStory(" + str(csbgnpy.pd.io.sbgnlog._entity_to_constant(e)) + ',' + str(i) + ").")

    ctrl.ground([("base", [])])

    models = []
    def on_model(model):
        models.append([str(atom).split('(')[1][:-1] for atom in model.symbols(shown=True)])
    ctrl.solve(on_model = on_model)
    return models
