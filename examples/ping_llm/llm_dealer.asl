!start.

+!start <-
    .name(N) ;
    .print("hello from", N).

+!request_nb_planets[source(X)] <-
    .prompt(nb_planets);
    +respond_to(X).

+respond_to(X) <-
    .print("waiting for llm response.").

+nb_planets(X)[source(llm)] : respond_to(D) <-
    .print("response received from llm, going to respond to", D);
    -respond_to(D) ;
    .autogen_send(D,tell,nb_planets(X)).
