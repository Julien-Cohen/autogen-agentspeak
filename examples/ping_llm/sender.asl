!start.

+!start <- .print("hello from sender").

+!do_request <-
    .print("I received a request.");
    .autogen_send(llm_dealer, achieve, request).

+nb_planets(X) <-
    .print("The number of planets is ", X).

