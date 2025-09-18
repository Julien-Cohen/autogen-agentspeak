!start.

pos(0).

+!start <-
    .set_public(do_move, 0, "Move the robot.") ;
    .set_public(do_jump, 0, "Make the robot jump.") ;
    .set_public(move_by, 1, "Move the robot by the distance given as parameter (in cm).") ;
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

+!move_by(D) : pos(X) <-
    .print("I received a move-by request.") ;
    -+pos(X+D) ;
    ?pos(Y) ;
    .print("I moved at pos", Y).

+!do_jump <-
    ?pos(P);
    .print("I received a jump request, while I am at pos", P);
    jump.
