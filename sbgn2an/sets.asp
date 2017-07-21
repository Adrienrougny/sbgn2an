#show incompat/2.

#program base.

process(P):-edge(X,Y,P).

belong_in(P,X,S):-inStory(X,S);inStory(Y,S);edge(X,Y,P).
belong_out(P,X,S):-inStory(X,S);inStory(Y,S);edge(Y,X,P).

incompat(S1,S2):-story(S1);story(S2);S1!=S2;inStory(X,S1):inStory(X,S2).

incompat(S2,S1):-incompat(S1,S2).
incompat(S1,S2):-story(S1);story(S2);inStory(X,S1);inStory(X,S2);process(P1);process(P2);belong_in(P1,X,S1);not belong_in(P1,X,S2);belong_in(P2,X,S2);not belong_in(P2,X,S1).



#program sets.

0 {inSet(S)} 1:-story(S).
:-story(S1);story(S2);inSet(S1);inSet(S2);incompat(S1,S2).

#program max_incl.

:-story(S1);not inSet(S1);not incompat(S2,S1):inSet(S2).
