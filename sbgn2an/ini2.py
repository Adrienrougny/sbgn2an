import clingo

import csbgnpy.pd.io.sbgnml
import csbgnpy.pd.io.sbgnlog
import sbgn2an.stories

def get_ini(net, stories = None):
    ctrl = clingo.Control(["--warn=none", "-n 0", "--opt-mode=opt"])
    # ctrl = clingo.Control(["-n 0"])
    ctrl.load(os.path.join(os.getcwd(), "ini.lp"))
    ctrl.load(os.path.join(os.getcwd(), "pd.lp"))
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
        models.append([atom.split('(')[1][:-1] for atom in model.symbols(shown=True)])
    return models
