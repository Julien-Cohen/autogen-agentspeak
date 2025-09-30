!start.

secret(42).

+!start <- .print("hello from sender").

+!do_ping : secret(X) <-
    .print("I received a ping request.");
    .send(to_receiver, achieve, show);
    .send(to_receiver, tell, secret(X));
    .wait(1000);
    .send(to_receiver, achieve, show);
    .send(to_receiver, untell, secret(X));
    .wait(1000);
    .send(to_receiver, achieve, show);
    .print("Done.").



