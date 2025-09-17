!start.

pos(0).

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!do_move : pos(X) <-
    .print("I received a move request.") ;
    -+pos(X+1) ;
    ?pos(Y) ;
    .print("I moved at pos", Y).

# Warning : the order of rules is important in AgentSpeak.
# First rule has priority (not best match).
+!do_move <- .print("failsafe plan for do_move").

+!do_jump <-
    ?pos(P);
    .print("I received a jump request, while I am at pos", P);
    jump.
