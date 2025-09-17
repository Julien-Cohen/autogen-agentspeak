!start.

+pos(0).

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!do_move <- .print("failsafe plan for do_move").

+!do_move : pos(X) <-
    .print("I received a move request.").
#    ;
#    -+pos(X+1) ;
#    ?pos(Y) ;
#    .print("I moved at pos", Y).

+!do_jump <-
    .print("I received a jump request");
    jump.
