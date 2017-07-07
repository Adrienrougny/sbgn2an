try:
    import clingo as gringo
    gringo_v = 5
except:
    import gringo
    gringo_v = 4

import sbgn2an.config

class Story(frozenset):
    def __str__(self):
        return "{{{}}}".format(','.join([e.id for e in list(self)]))
    pass

class StoriesControl(object):
    def __init__(self, net):
        self.net = net
        self.models = []

    def solve(self, on_story = None, same_labels = True, only_max = True, n = 0):
        asp = sbgn2an.utils.cg2asp(self.net)
        asp = sorted(asp)
        for atom in asp:
            print(atom)
        # seed = sbgn2an.utils.get_seeds(self.net, n = 1)[0]
        ctrl = gringo.Control()
        ctrl.configuration.solve.models = n
        ctrl.load(sbgn2an.config.STORIES_FILE)
        # for rule in asp:
        #     ctrl.add("base", [], rule)
        # for epn in seed:
        #     ctrl.add("base", [], "seed({0}).".format(epn))
        ctrl.ground([("base", [])])
        if same_labels:
            ctrl.ground([("same_labels", [])])
        self.on_story = on_story
        res = ctrl.solve(on_model = self._on_model)
        print(len(self.models))

    def _on_model(self, model):
        self.models.append(model)
        if self.on_story is not None:
            story = self._parse_model(model)
            if story is not None:
                self.on_story(story)

    def _parse_model(self, model):
        label = None
        story = []
        if gringo_v == 4:
            lits = [str(lit) for lit in model.atoms()]
        else:
            lits = [str(lit) for lit in model.symbols(atoms = True)]
        for lit in lits:
            if lit.startswith("inStory"):
                entity = None
                eid = lit[:-1].split('(')[1]
                for entity in self.net.entities:
                    if entity.id == eid:
                        break
                story.append(entity)
        story = Story(story)
        return story

def get_stories(net, same_labels = True, only_max = True, n = 0):
    stories = []
    def on_story(story):
        stories.append(story)
    ctrl = StoriesControl(net)
    ctrl.solve(on_story, same_labels, only_max, n)
    return stories
