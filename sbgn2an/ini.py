from csbgnpy.pd.process import Process

import networkx

try:
    import clingo as gringo
    gringo_v = 5
except:
    import gringo
    gringo_v = 4

import sbgn2an.config

class IniControl(object):
    def __init__(self, net, rem_inhib = True):
        self.net = net
        self.rem_inhib = rem_inhib
        self._initialize()

    def _initialize(self):
        self.all_choices = []
        ini = sbgn2an.utils.get_sources(self.net)
        if self.rem_inhib:
            toremove = set()
            for e in ini:
                isinhib = False
                for m in self.net.modulations:
                    if isinstance(m, Inhibition) and m.source == e:
                        isinhib = True
                        break
                if isinhib:
                    toremove.add(e)
            for e in toremove:
                ini.remove(e)
        self.ini = ini
        sccs = sbgn2an.utils.get_sccs(self.net)
        for scc in sccs:
            if len(scc) > 1:
                choices = [list(set(node.reactants)) for node in scc if isinstance(node, Process)]
                for choice in choices:
                    toadd = False
                    for e in ini:
                        if e in choice:
                            toadd = True
                            break
                    if toadd:
                        for e in choice:
                            self.ini.add(e)
                        break
                if not toadd:
                    self.all_choices.append(choices)

    def reset(self):
        self._initialize()

    def select(self, choice):
        toremove = []
        for choices in self.all_choices:
            rem = False
            for choice2 in choices:
                toadd = False
                for e in choice:
                    if e in choice2:
                        toadd = True
                        rem = True
                        break
                if toadd:
                    for e in choice2:
                        self.ini.add(e)
            if rem:
                toremove.append(choices)
        for choices in toremove:
            self.all_choices.remove(choices)
        for e in choice:
            self.ini.add(e)

    def get_next_choice(self):
        if self.all_choices:
            return self.all_choices[0]
        return None

    def ui(self):
        while self.get_next_choice():
            choices = self.get_next_choice()
            for i, choice in enumerate(choices):
                print("{}: {}".format(i, choice))
            j = int(input("Choice: "))
            self.select(choices[j])
        print(self.ini)

