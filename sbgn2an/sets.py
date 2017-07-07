import gringo
import sbgn2an.config
import sbgn2an.utils

class Story(frozenset):
    def __init__(self, it = None, label = None):
        if it super().__init(it)
        self.label = label

class StoriesControl(object):
    def __init__(self, net):
        self.net = net
        self.conf = n
        self.asp = sbgn2an.utils.cg2asp(self.net)
        self.ctrl = gringo.Control()
        self.ctrl.conf.solve.models = self.conf
        self.ctrl.load(sbgn2an.config.STORIES_FILE)
        for rule in self.asp:
            self.ctrl.add("base", [], rule)
        for epn in self.seed:
            self.ctrl.add("base", [], "seed({0}).".format(epn))
        self.ctrl.ground([("base", [])])

    def solve(self, on_story = None, only_max = True, same_labels = True, n = 0):
        asp = sbgn2an.utils.cg2asp(self.net)
        seed = sbgn2an.utils.get_seeds(net, n = 1)[0]
        ctrl = gringo.Control()
        ctrl.conf.solve.models = n
        ctrl.load(sbgn2an.config.STORIES_FILE)
        for rule in self.asp:
            ctrl.add("base", [], rule)
        for epn in self.seed:
            ctrl.add("base", [], "seed({0}).".format(epn))
        ctrl.ground([("base", [])])
        if only_max:
            ctrl.ground([("only_max", [])])
        if same_labels:
            ctrl.ground([("same_labels", [])])
        self.on_story = on_story
        res = ctrl.solve(on_model = self._on_model)

    def _on_model(self, model):
        if self.on_story is not None:
            story = self._parse_model(model)
            if story is not None:
                self.on_story(story)

    def _parse_model(self, model):
        label = None
        story = []
        for lit in [str(lit) for lit in model.atoms()]:
            if lit.startswith("chosen"):
                label = lit[:-1].split('(')[1]
            if lit.startswith("inStory"):
                story.append(lit[:-1].split('(')[1])
        if len(story) <= 1:
            story = None
        else:
            story = Story(story, label)
        return story

# class SetsControl(object):
#     def __init__(self, net, n = 0):
#         self.net = net
#         self.asp = sbgn2an.utils.cg2asp(self.net)
#         self.ctrl = gringo.Control()
#         self.ctrl.conf.solve.models = 0
#         self.ctrl.load(sbgn2an.config.SETS_FILE)
#         for rule in self.asp:
#             self.ctrl.add("base", [], rule)
#
#     def solve(self, stories = None, on_set = None, max_epn = True):
#         self.on_set = on_set
#         if stories is not None:
#             for story in stories:
#                 for i in range(len(stories) - 1):
#                     self.ctrl.add("base", [], "gather({0},{1}).".format(story[i], story[i+1]))
#                 self.ctrl.add("base", [], "gather({0},{1}).".format(story[-1], story[0]))
#         if max_epn:
#             self.ctrl.load(sbgn2an.config.MAX_FILE)
#             self.ctrl.conf.solve.opt_mode = "optN"
#         self.ctrl.ground([("base", [])])
#         res = self.ctrl.solve(on_model = self._on_model)
#
#     def _on_model(self, model):
#         sset = self._parse_model(model)
#         if self.on_set is not None and sset is not None:
#             self.on_set(sset)
#
#     def _parse_model(self, model):
#         preSet = []
#         for literal in [str(literal) for literal in model.atoms()]:
#             if "gather" in literal:
#                 pair = literal[:-1].split("gather(")[1].split(",")
#                 added = False
#                 for s in preSet:
#                     if pair[0] in s and pair[0] != "emptyset":
#                         s.add(pair[1])
#                         added = True
#                         break
#                     elif pair[1] in s and pair[1] != "emptyset":
#                         s.add(pair[0])
#                         added = True
#                         break
#                 if added is False:
#                     preSet.append(set([pair[0],pair[1]]))
#         i = 0
#         while i <= len(preSet) -1:
#             s = preSet[i]
#             j = i+1
#             while j <=  len(preSet) -1:
#                 q = preSet[j]
#                 if len(s & q) != 0 and s & q != set(["emptyset"]):
#                     s = s | q
#                     preSet[i] = s
#                     del preSet[j]
#                 else:
#                     j += 1
#             i += 1
#         sset = []
#         for story in preSet:
#             sset.append(list(story))
#         if not sset:
#             return None
#         return sset


def get_maximal_stories(net, n = 0):
    stories = []
    def on_story(label, story):
        stories.append((label, story))
    ctrl = StoriesControl(net, n)
    ctrl.solve(on_story = on_story)
    return stories

def get_sets_of_stories(net, stories = None, max_epn = True, n = 0):
    sets = []
    def on_set(sset):
        sets.append(sset)
    ctrl = SetsControl(net, n)
    ctrl.solve(stories, on_set, max_epn)
    return sets
