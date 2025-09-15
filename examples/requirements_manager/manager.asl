!start.

+!start <-
    .name(N) ;
    .print("hello from", N).

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

+new_req(N) : req([L]) <-
    .print("New requirement received:", N) ;
     .print("(A) Old list contains", L) ;
    -new_req(N) ;
    -req([L]) ;
    +req([N|L]) ;
    !build.

+new_req(N) : req([]) <-
    .print("New requirement received:", N) ;
    .print("(B) Old list is empty") ;
    -new_req(N) ;
    -req([]);
    +req([N]) ;
    !build.

+new_req(N) : req(L) <-
    .print("New requirement received:", N) ;
    .print("(C) Old list is", L) ;
    -new_req(N) ;
    -req(L);
    +req([N|L]) ;
    !build.
#+req(L) <-
#    .print("Status of requirements:", L).