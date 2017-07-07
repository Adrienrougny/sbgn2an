#show gather/3.

%epn(node_id) an EPN with node id node_id 
%belong(label,node_id) EPN node_id contains the label label 
%edge(node_id1,node_id2,edge_id) the process edge_id consumes the EPN node_id1 and produces the EPN node_id2
%gather(node_id1,node_id2,edge_id) the EPNs node_id1 and node_id2 belong to the same story

hasLabel(X):-labeled(X,L).
inStory(X):-gather(X,Y).
inStory(X):-gather(Y,X).

%constraint (i) and (ii) + story generator
%we gather together two epns linked by a process, or not

0 {gather(X,Y,E)} 1:-edge(X,Y,E);epn(X);epn(Y);X!=Y.

%constraint (ii)
% if an EPN of the story is a product of a process, then at least one reactant of that process belongs to the story

%constraint (iii)
%for two EPNs of the story, there exist no process that consumes both of them

:-edge(Z,X,E);edge(Y,X,E);gather(Y,Z,_);Z!=Y.

%constraint (iv)
%for two EPNs of the story, there exist no process that produces both of them

:-edge(X,Z,E);edge(X,Y,E);gather(Y,Z,_);Z!=Y.

%constraint (v)
%1 {cand(L,X):labeled(X,L)} 1:-hasLabel(X);epn(X).
%sameLabel(X,Y):-cand(L,Y);cand(L,X);epn(X);epn(Y);X!=Y.
%:-not sameLabel(X,Y);gather(X,Y);epn(X);epn(Y);X!=Y.

c5(X):-labeled(Y,L):gather(X,Y);labeled(X,L);gather(X,_);labeled(_,L).
:-not c5(X);gather(X,_).
