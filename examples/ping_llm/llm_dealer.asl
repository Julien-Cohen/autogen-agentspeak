!start.

+!start <-
    .print("hello from llm dealer").

+!request[source(X)] <-
    .prompt(hello);
    +respond_to(X).

+respond_to(X) <-
    .print("waiting for llm response.").

+nb_planets(X) : respond_to(D) <-
    .print("response received from llm, going to respond to ", D);
    -respond_to(D) ;
    .autogen_send(D,tell,nb_planets(X)).
