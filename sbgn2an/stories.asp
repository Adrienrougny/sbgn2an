%%%%computes all stories%%%%

#show inStory/1.

#program base.

label(L):-labeled(X,L).
isProduced(X):-edge(Y,X,E);epn(X).
isConsumed(X):-edge(X,Z,E);epn(X).

%candidate generation and (i)
0 {inStory(X)} 1:-epn(X).

%constraint (i)

c1(Y,X):-c1(X,Y).
c1(X,Y):-epn(X);epn(Y);inStory(X);inStory(Y);edge(X,Y,_).
c1(X,Z):-epn(X);epn(Y);epn(Z);c1(X,Y);inStory(Z);edge(Y,Z,_).
c1(X,Z):-epn(X);epn(Y);epn(Z);c1(X,Y);inStory(Z);edge(Z,Y,_).
:-not c1(X,Y);X!=Y;inStory(X);inStory(Y);epn(X);epn(Y).

%constraint (ii)

c2(X):-not isProduced(X);inStory(X);epn(X).
c2(X,P):-edge(Y,X,P);inStory(Y);inStory(X);epn(Y);epn(X).
:-not c2(X,P);edge(_,X,P);inStory(X);epn(X).

%constraint (iii)
:-inStory(Y);inStory(X);X!=Y;edge(X,Z,E);edge(Y,W,E);epn(X);epn(Y);epn(Z);epn(W).

%constraint (iv)
:-inStory(Y);inStory(X);X!=Y;edge(Z,X,E);edge(W,Y,E);epn(X);epn(Y);epn(Z);epn(W).

#program same_labels.

%constraint (v)

optSameLabels.
sameLabels:-labeled(X,L):inStory(X);label(L).
:-not sameLabels.

#program max_incl.

%if there is an epn, emptyset is not a max story
:-not inStory(Y):epn(Y);epn(X).

negc3(X):-inStory(Y);X!=Y;edge(X,Z,E);edge(Y,W,E);epn(X);epn(Y);epn(Z);epn(W).
c3(X):-epn(X);not negc3(X).
negc4(X):-inStory(Y);X!=Y;edge(Z,X,E);edge(W,Y,E);epn(X);epn(Y);epn(Z);epn(W).
c4(X):-epn(X);not negc4(X).

%if not same_labels
:-not optSameLabels;epn(X);epn(Y);inStory(X);not inStory(Y);edge(X,Y,_);c3(Y);c4(Y).

%if same_labels
chosen(L):-labeled(X,L):inStory(X);label(L);optSameLabels.
c5(X):-epn(X);chosen(L);labeled(X,L);optSameLabels.
:-optSameLabels;epn(X);epn(Y);inStory(X);not inStory(Y);edge(X,Y,_);c3(Y);c4(Y);c5(Y).
