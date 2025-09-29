!start.

secret(42).

+!start <-
    .print("hello from sender").

+!do_ping <-
    .print("I received a ping request.");
    .send(to_receiver, tell, sender_alive);
    .wait(1000);
    .print("Sent.").



+!share_secret : secret(X) <-
    .send(to_receiver, tell, secret(X)).

