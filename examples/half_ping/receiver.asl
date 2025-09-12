!start.

+!start <-
    .print("hello from receiver").

+sender_alive[source(S)] <-
    .print("new belief : the sender is alive (from", S, ")");
    .autogen_send(S, tell, pong).
