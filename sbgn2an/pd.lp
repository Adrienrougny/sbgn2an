modulates_pd(A,B):-stimulates_pd(A,B).
modulates_pd(A,B):-inhibits_pd(A,B).
stimulates_pd(A,B):-necessarilyStimulates_pd(A,B).
stimulates_pd(A,B):-catalyzes_pd(A,B).

logicalOperator_pd(O):-and_pd(O).
logicalOperator_pd(O):-or_pd(O).
logicalOperator_pd(O):-not_pd(O).

epn_pd(E):-macromolecule_pd(E).
epn_pd(E):-unspecifiedEntity_pd(E).
epn_pd(E):-simpleChemical_pd(E).
epn_pd(E):-nucleicAcidFeature_pd(E).
epn_pd(E):-perturbation_pd(E).
epn_pd(E):-complex_pd(E).

subEntity_pd(E):-subMacromolecule_pd(E).
subEntity_pd(E):-subUnspecifiedEntity_pd(E).
subEntity_pd(E):-subSimpleChemical_pd(E).
subEntity_pd(E):-subNucleicAcidFeature_pd(E).
subEntity_pd(E):-subComplex_pd(E).

process_pd(P):-phenotype_pd(P).
process_pd(P):-association_pd(P).
process_pd(P):-dissociation_pd(P).
process_pd(P):-omittedProcess_pd(P).
process_pd(P):-unknownProcess_pd(P).
