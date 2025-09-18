!start.

pos(0).

+!start <-
    .set_public(do_move,0, "move the robot") ;
    .set_public(do_jump,0, "make the robot jump") ;
    .my_name(N) ;
    .print("hello from", N).

+!publish[source(S)] <-
    .print("Going to publish my catalog") ;
    .send_catalog(S).

+!do_move : pos(X) <-
    .print("I received a move request.") ;
    -+pos(X+1) ;
    ?pos(Y) ;
    .print("I moved at pos", Y).

+!do_jump <-
    ?pos(P);
    .print("I received a jump request, while I am at pos", P);
    jump.
