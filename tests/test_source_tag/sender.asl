!start.

secret(42).

+!start <- .print("Hello from sender").

+!share_secret : secret(X) <-
    .autogen_send(to_receiver, tell, secret(X), ANSWER).

