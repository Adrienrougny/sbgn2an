%#show choose/1.
%compute seeds

epn(a).
epn(b).
edge(a,b,e1).
%edge(b,a,e2).

path(E1,E2):-edge(E1,E2,_).
path(E1,E3):-path(E1,E2);edge(E2,E3,_).
scc(E1,E2):-path(E1,E2);path(E2,E1).
scc(E,E):-epn(E).

source(E):-epn(E);not edge(_,E,_).
covered(E):-source(E).
covered(E2):-covered(E1):edge(E1,E2,P);edge(_, E2, P).


1 {chosenSccEpn(E2):scc(E2,_)} 1.

%1 {chosenSccEpn(E2):scc(E2,_), not covered(E2)} 1:-scc(E1,_);not covered(E1).
chosenScc(E):-chosenSccEpn(E).
chosenScc(E2):-chosenSccEpn(E1);scc(E1,E2).
choose(E):-chosenScc(E);source(E).

1 {choose(E2):chosenScc(E2),not covered(E2)}:-chosenScc(E1);not covered(E1).

coveredForScc(E):-covered(E).
coveredForScc(E):-choose(E).
coveredForScc(E2):-coveredForScc(E1):edge(E1,E2,P);edge(_, E2, P).
:-chosenScc(E);not coveredForScc(E).
