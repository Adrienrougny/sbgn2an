#show inIni/1.
%#show score/2.
%#show covered/1.
0 {inIni(E)} 1:-epn(E).
covered(E):-inIni(E).
:-epn(E);not covered(E).
covered(E):-covered(E'):edge(E',E,P);edge(_,E,P).

score(E,C,N-M):-epn(E);C={complex(E)};M={sv(E,unset,Var)};N={sv(E,Val,Var)}.

:-inIni(E);inIni(E');E!=E';inStory(E,S);inStory(E',S).

#minimize {C@3,E:score(E,C,N),inIni(E),epn(E)}.
#minimize {N@2,E:score(E,C,N),inIni(E),epn(E)}.
#minimize {1@1,E : inIni(E)}.
