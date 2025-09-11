!start.

secret(42).

+!start <- .print("hello from sender").

+!do_request <-
    .print("I received a request.");
    .autogen_send(to_receiver, achieve, request, _);
    .wait(1000);
    .print("sent.").



+nb_planets(X) <-
    .print("The number of planets is ", X).

