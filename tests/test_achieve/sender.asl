!start.

secret(42).

+!start <- .print("(sender/asp layer) hello from sender").

+!do_ping <-
    .print("(sender/asp layer) I received a ping request.");
    .autogen_send(to_receiver, tell, sender_alive);
    .wait(1000);
    .print("(sender/asp layer) sent.").



+!share_secret : secret(X) <-
    .autogen_send(to_receiver, tell, secret(X)).

