%compute seeds
0 {seed(E)} 1 :- epn(E).
cov(E) :- seed(E).
cov(E):-cov(E'):edge(E',E,P); edge(_, E, P).
:- not cov(E); epn(E).

#minimize {1,E : seed(E)}.
