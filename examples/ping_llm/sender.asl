!start.

+!start <-
    .name(N) ;
    .print("hello from", N).

+!do_request <-
    .print("I received a request.");
    .autogen_send(llm_dealer, achieve, request_nb_planets).

+nb_planets(X) <-
    .print("The number of planets is", X).

