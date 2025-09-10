!start.

secret(42).

+!start <- .print("hello from sender").

+!do_ping : secret(X) <-
    .print("I received a ping request.");
    .autogen_send(to_receiver, achieve, show, ANSWER);
    .autogen_send(to_receiver, tell, secret(X), ANSWER);
    .wait(1000);
    .autogen_send(to_receiver, achieve, show, ANSWER);
    .autogen_send(to_receiver, untell, secret(X), ANSWER);
    .wait(1000);
    .autogen_send(to_receiver, achieve, show, ANSWER);
    .print("Done.").



