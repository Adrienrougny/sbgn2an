from collections import defaultdict

try:
    import clingo as gringo
    gringo_v = 5
except:
    import gringo
    gringo_v = 4

import sbgn2an.config

class Story(list):
    def __str__(self):
        return "{{{}}}".format(','.join([str(e.id) for e in list(self)]))

    def get_labels(self):
        labels = []
        d = defaultdict(int)
        for e in self:
            done = []
            if hasattr(e, "label"):
                d[e.label] += 1
            if hasattr(e, "components"):
                for sube in e.components:
                    if hasattr(sube, "label") and sube.label not in done:
                        d[sube.label] += 1
                        done.append(sube.label)
        for label in d.keys():
            if d[label] == len(self):
                labels.append(label)
        return labels

class StoriesControl(object):
    def __init__(self, net):
        self.net = net

    def solve(self, on_story = None, same_labels = False, only_max = False, n = 0):
        asp = sbgn2an.utils.cg2asp(self.net)
        ctrl = gringo.Control(["--warn=none"])
        ctrl.configuration.solve.models = n
        ctrl.load(sbgn2an.config.STORIES_FILE)
        for rule in asp:
            ctrl.add("base", [], rule)
        ctrl.ground([("base", [])])
        if same_labels:
            ctrl.ground([("same_labels", [])])
        if only_max:
            ctrl.ground([("max_incl", [])])
        self.on_story = on_story
        res = ctrl.solve(on_model = self._on_model)

    def _on_model(self, model):
        if self.on_story is not None:
            story = self._parse_model(model)
            if story is not None:
                self.on_story(story)

    def _parse_model(self, model):
        story = []
        if gringo_v == 4:
            atoms = [str(atom) for atom in model.atoms()]
        else:
            atoms = [str(atom) for atom in model.symbols(atoms = True)]
        for atom in atoms:
            if atom.startswith("inStory"):
                entity = None
                eid = atom[:-1].split('(')[1]
                for entity in self.net.entities:
                    if entity.id == eid:
                        break
                story.append(entity)
        story = Story(story)
        return story

def get_stories(net, same_labels = False, only_max = False, allow_singletons = False, n = 0):
    if only_max:
        n = 0
    stories = []
    def on_story(story):
        if not allow_singletons:
            if len(story) > 1 and story not in stories:
                stories.append(story)
        else:
            if story not in stories:
                stories.append(story)
    # def on_story(story):
    #     add = True
    #     to_remove = []
    #     if not only_max:
    #         stories.add(story)
    #     else:
    #         for story2 in stories:
    #             if story2.issuperset(story):
    #                 add = False
    #                 break
    #             elif story2.issubset(story):
    #                 to_remove.append(story2)
    #     for story2 in to_remove:
    #         stories.remove(story2)
    #     if add:
    #         stories.add(story)
    ctrl = StoriesControl(net)
    ctrl.solve(on_story, same_labels, only_max, n)
    return stories
