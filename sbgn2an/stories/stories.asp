#show inStory/1.
#show chosen/1.
#show c5/1.
#show sameLabel/2.
#show c3/1.
#show c4/1.
#show c2/1.
#show c1/1.
#show isConsumed/1.
#show isProduced/1.
#show seed/1.
#show first/1.
#show candidate/1.
#show isStory/0.

1 {first(X):seed(X)} 1.
candidate(X):-first(X).
node(X):-epn(X).
%node(emptyset).


isProduced(X):-edge(Y,X,E);node(X).
isConsumed(X):-edge(X,Z,E);node(X).
sameLabel(X,Y):-labeled(X,L);labeled(Y,L);epn(Y);epn(X).
label(L):-labeled(X,L).

%contraint (i)
c1(X):-edge(Y,X,E);candidate(Y);node(X).
c1(X):-edge(X,Y,E);candidate(Y);node(X).

%constraint (ii)

c2(X):-candidate(Y);edge(Y,X,E);node(X).
c2(X):-not isProduced(X);node(X).

%constraint (iii)

negC3(X):-candidate(Y);X!=Y;edge(X,Z,E);edge(Y,W,E);node(X);node(Y);node(Z);node(W).
c3(X):-not negC3(X);node(X).
c3(X):-not isConsumed(X);node(X).

%constraint (iv)

negC4(X):-candidate(Y);X!=Y;epn(X);epn(Y);edge(Z,X,E);edge(W,Y,E);node(X);node(Y);node(Z);node(W).
c4(X):-not negC4(X);node(X).
c4(X):-not isProduced(X);node(X).

%constraint (v)

negC5(X):-not sameLabel(X,Y);candidate(Y);epn(Y);epn(X).
c5(X):-not negC5(X);epn(X).

%candidate(emptyset):-c1(emptyset);c2(emptyset);c3(emptyset);c4(emptyset).
candidate(X):-c1(X);c2(X);c3(X);c4(X);c5(X);epn(X).

isStory:-c1(X);c2(X);c3(X);c4(X);c5(X);first(X).

inStory(X):-candidate(X);isStory.

chosen(L):-labeled(X,L):inStory(X),epn(X);label(L).
