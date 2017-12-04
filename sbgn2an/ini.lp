#show inIni/1.
%#show score/2.
%#show covered/1.
0 {inIni(E)} 1:-epn_pd(E).
covered(E):-inIni(E).
:-epn_pd(E);not covered(E).
covered(E):-epn_pd(E);process_pd(P);produces_pd(P,E,_);covered(E'):consumes_pd(P,E',_).

score(E,C,N-M):-epn_pd(E);C={complex_pd(E)};M={stateVariable_pd(E,unset_pd,Var)};N={stateVariable_pd(E,Val,Var)}.

:-inIni(E);inIni(E');E!=E';inStory(E,S);inStory(E',S).

#minimize {C@3,E:score(E,C,N),inIni(E),epn_pd(E)}.
#minimize {N@2,E:score(E,C,N),inIni(E),epn_pd(E)}.
#minimize {1@1,E : inIni(E)}.
