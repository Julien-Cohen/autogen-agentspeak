!start.

+!start <-
    .name(N) ;
    .print("hello from", N).

+!run_test_list <-
    L= [1,2] ;
    .print("Test") ;
    .print(L) ; # [ 1,2 ]
    [0|L]=M ;
    .print(M); # [0 | [1,2] ]
    .nth(0,M,R0) ; .print(R0); # 0
    .nth(1,M,R1) ; .print(R1); # 1
    .nth(2,M,R2) ; .print(R2) ; # 2
    .print("test1");
    for (.member(X,L)) {.print(X);}; # 1  2
    .print("test2");
    for (.member(X,M)) {.print(X);}. # 0 fail


+spec(S) <-
    .print("I received the specification to manage:", S).

+!build : spec(S) & not req(_) <-
    .print("No list of requirements found, creating an empty list.");
    +req([]) ;
    !build.

+!build : spec(S) & req(L) <-
    .print("List of requirements found. Going to ask for completeness.", L) ;
    .autogen_send(to_completeness_evaluator, tell, req(L)) ;
    .autogen_send(to_completeness_evaluator, achieve, evaluate).

+completeness(true) : req(L) <-
    .print("List of requirements complete:", L).

+completeness(false) : spec(S) & req(L) <-
    .print("List of requirements not complete") ;
    .autogen_send(to_generator, tell, spec(S)) ;
    .autogen_send(to_generator, tell, req(L)) ;
    .autogen_send(to_generator, achieve, generate).

#+new_req(N) : req([L]) <-
#    .print("New requirement received:", N) ;
#     .print("(A) Old list contains", L) ;
#    -new_req(N) ;
#    -req([L]) ;
#    +req([N,L]) ;
#    !build.

#+new_req(N) : req([]) <-
#    .print("New requirement received:", N) ;
#    .print("(B) Old list is empty") ;
#    -new_req(N) ;
#    -req([]);
#    +req([N]) ;
#    !build.

+new_req(N) : req(L) <-
    .print("New requirement received:", N) ;
    .length(L,RES) ;
    .print("(C) Old list is", L, "len", RES) ;
    .print("test") ;
    .print([N,L]) ;
    .print([N|L]) ;
    -new_req(N) ;
    -req(L);
    +req([N|L]) ; # depending on if we use , or | here, we should decompose the list with , or | when translating AgentSpeak list into python lists.
                   # , makes difficult to handle sentences with commas, and | makes nested tuples
    !build.

+req(L) <-
    .print("Status of requirements:", L).