
import itertools
import sys

class Lit:
        def __init__(self, name, pos=True):
                self.__name = name
                self.__pos = pos
        @property
        def name(self):        
                return self.__name
        id = name
        @property
        def ispos(self):
                return self.__pos
        @property
        def isneg(self):
                return not self.__pos
        def __repr__(self):
                return "%s%s" % ("!" if not self.__pos else "", self.__name)
        def neg(self):
                return Lit(self.__name, not self.__pos)
        
        def __eq__(self, l):
                if not isinstance(l, Lit):
                        return False
                return l.__name == self.__name and l.__pos == self.__pos
        def __hash__(self):
                return hash((self.__name, self.__pos))

class AndClause(set):
        def __init__(self, *lits):
                if False in lits:
                        self.add(False)
                else:
                        for lit in lits:
                                if lit.neg() in self:
                                        self.clear()
                                        break
                                else:
                                        self.add(lit)
        def __hash__(self):
                return hash(tuple(self))

        def __repr__(self):
                if False in self:
                        return "false"
                elif len(self) == 0:
                        return "true"
                else:
                        return " and ".join([repr(l) for l in self])

        def copy(self):
            return AndClause(*set.copy(self))

        def __and__(c1, c2):
            return AndClause(*c1.union(c2))

        def __iand__(self, c2):
            self.update(c2)
            return self
        
        def inv(self):
                return AndClause(*[l.neg() for l in self])


class DNF(set):
        def __init__(self, *ands):
            self.update(ands)
            self.simplify()
        
        def __repr__(self):
                if len(self) == 0:
                        return "false"
                elif len(self) == 1:
                        return repr(list(self)[0])
                else:
                        return " or ".join(["(%s)" % repr(andc) if len(andc) > 1 else repr(andc) \
                                                                        for andc in self])
        
        def __or__(dnf1, dnf2):
                dnf = DNF(*dnf1.union(dnf2))
                dnf.simplify()
                return dnf
        
        def __ior__(self, dnf2):
                self.update(dnf2)
                self.simplify()
                return self

        def __and__(dnf1, dnf2):
            dnf = DNF()
            for andc1 in dnf1:
                for andc2 in dnf2:
                    dnf.add(AndClause(*andc1.union(andc2)))
            dnf.simplify()
            return dnf
        
        def simplify(self):
                try:
                        self.remove(AndClause(False))
                except KeyError:
                        pass
                andc = list(sorted(self, key=len))
                while len(andc):
                        largest = andc.pop()
                        if largest.inv() in andc:
                                self.clear()
                                self.add(AndClause())
                                break
                        for c in andc:
                                if largest.issuperset(c):
                                        self.remove(largest)
                                        break
        
        def neg(self):
                dnf = DNF(*map(lambda x: AndClause(*map(lambda l: l.neg(), x)), itertools.product(*self)))
                dnf.simplify()
                return dnf


if __name__ == "__main__":

        #expr1 = DNF(AndClause(Lit("B",False), Lit("C")), AndClause(Lit("D")))
        #expr2 = DNF(AndClause(Lit("D"), Lit("E")), AndClause(Lit("E"), Lit("F")))
        expr1 = DNF(AndClause(Lit("B"),Lit("C")), AndClause(Lit("B"),Lit("D")))
        expr2 = DNF(AndClause(Lit("B"),Lit("C")), AndClause(Lit("C"),Lit("D")))

        expr = expr1 | expr2

        nexpr = expr1.neg() | expr2.neg()

        print(expr1)
        print(expr2)
        print("---")
        print(expr)
        print(nexpr)

