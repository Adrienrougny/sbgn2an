%%%%computes all stories%%%%

#show inStory/1.
#show label/1.

#program base.
label(L):-labeled(X,L).
isProduced(X):-edge(Y,X,E);epn(X).
isConsumed(X):-edge(X,Z,E);epn(X).

%candidate generation and (i)
0 {inStory(X)} 1:-epn(X).

%constraint (i)

path(X,Y):-edge(X,Y,_).
path(X,Z):-path(X,Y);path(Y,Z).
uPath(X,Y):-path(X,Y).
uPath(Y,X):-uPath(X,Y).
:-inStory(X);inStory(Y);not uPath(X,Y).

%constraint (ii)

:-not inStory(Y):edge(Y,X);isProduced(X);inStory(X);epn(X).

%c2(X):-not isProduced(X);inStory(X);epn(X).
%c2(X):-edge(Y,X,_);inStory(Y);inStory(X);epn(Y);epn(X).
%:-not c2(X);inStory(X);epn(X).

%constraint (iii)
:-inStory(Y);inStory(X);X!=Y;edge(X,Z,E);edge(Y,W,E);epn(X);epn(Y);epn(Z);epn(W).

%constraint (iv)
:-inStory(Y);inStory(X);X!=Y;edge(Z,X,E);edge(W,Y,E);epn(X);epn(Y);epn(Z);epn(W).

;edge(Y,X,E);inStory(Y);not inStory(X);epn(X).

#program same_labels.

%constraint (v)
sameLabel:-labeled(X,L):inStory(X);label(L).
:-not sameLabel.

#only_max.

negC3:-inStory(Y);not inStory(X);X!=Y;edge(X,Z,E);edge(Y,W,E);epn(X);epn(Y);epn(Z);epn(W).

epn(X);epn(Y);not inStory(X);inStory(Y);uPath(X,Y)
