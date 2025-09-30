!start.

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+spec(S)[source(F)] <-
    +from(F) ;
    .print("I received the specification to manage:", S).

+!build : spec(S) & not req(_) <-
    .print("No list of requirements found, creating an empty list.");
    +req([]) ;
    !build.

+!build : spec(S) & req(L) <-
    .print("List of requirements found. Going to ask for completeness.", L) ;
    .send(to_completeness_evaluator, tell, spec(S)) ;
    .send(to_completeness_evaluator, tell, req(L)) ;
    .send(to_completeness_evaluator, achieve, evaluate).

+completeness(true) : req(L) & from(F)<-
    .print("List of requirements complete:", L) ;
    .print("Sent to", F);
    .send(F, tell, req(L)).

+completeness(false) : spec(S) & req(L) <-
    .print("List of requirements not complete") ;
    .send(to_generator, tell, spec(S)) ;
    .send(to_generator, tell, req(L)) ;
    .send(to_generator, achieve, generate).

+new_req(N) : req(L) <-
    .print("New requirement received:", N) ;
    .length(L,RES) ;
    .print("Old list is", L, "len", RES) ;
    -new_req(N) ;
    -req(L);
    +req([N|L]) ; # depending on if we use , or | here, we should decompose the list with , or | when translating AgentSpeak list into python lists.
                   # , makes difficult to handle sentences with commas, and | makes nested tuples
    !build.

+req(L) <-
    .print("Status of requirements:", L).

+from(F) <-
    .print("Reply-to:", F).
    