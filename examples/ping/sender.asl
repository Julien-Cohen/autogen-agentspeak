!start.

secret(42).

+!start <- .print("Hello from sender").

+!do_ping <-
    .print("I received a ping request.");
    .autogen_send(to_receiver, tell, sender_alive);
    .wait(1000);
    .print("Sent.").



+!share_secret : secret(X) <-
    .autogen_send(to_receiver, tell, secret(X)).

