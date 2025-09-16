!start.

secret(42).

+!start <-
    .my_name(N);
    .print("Hello from", N).

+!share_secret : secret(X) <-
    .autogen_send(to_receiver, tell, secret(X)).

