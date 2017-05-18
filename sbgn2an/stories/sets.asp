#show gather/2.

%epn(node_id) an EPN with node id node_id 
%belong(label,node_id) EPN node_id contains the label label 
%edge(node_id1,node_id2,edge_id) the process edge_id consumes the EPN node_id1 and produces the EPN node_id2
%gather(node_id1,ode_id2) the EPNs node_id1 and node_id2 belong to the same story

hasLabel(X):-labeled(X,L).
inStory(X):-gather(X,Y).
inStory(X):-gather(Y,X).
node(X):-epn(X).
%node(emptyset).

%the gather relation is symmetric and transitive
gather(Y,X):-gather(X,Y).
gather(X,Z):-gather(X,Y);gather(Y,Z);epn(Y);X!=Z;node(X);node(Z).

%constraint (i) + story generator
%we gather together two epns linked by a process, or not

0 {gather(X,Y)} 1:-edge(X,Y,E);node(X);node(Y);X!=Y.

%constraint (ii)
% if an EPN of the story is a product of a process, then at least one reactant of that process belongs to the story

good(X,E):-edge(Y,X,E);gather(X,Y);inStory(X).
:-not good(X,E);edge(Z,X,E);epn(X);inStory(X).
%notGood(X,E,L):-not good(X,E);edge(Z,X,E);labeled(X,L);inStory(X).
%good(X,E):-edge(Y,X,E);gather(X,Y).
%:-not good(X,E);edge(Z,X,E);gather(X,Y);X!=Y.

%constraint (iii)
%for two EPNs of the story, there exist no process that consumes both of them

:-gather(X,Y);edge(X,Z,E);edge(Y,W,E);X!=Y.

%constraint (iv)
%for two EPNs of the story, there exist no process that consumes both of them

:-gather(X,Y);edge(Z,X,E);edge(W,Y,E);X!=Y.

%constraint (v)
1 {cand(L,X):labeled(X,L)} 1:-hasLabel(X);epn(X).
sameLabel(X,Y):-cand(L,Y);cand(L,X);epn(X);epn(Y);X!=Y.
:-not sameLabel(X,Y);gather(X,Y);epn(X);epn(Y);X!=Y.
