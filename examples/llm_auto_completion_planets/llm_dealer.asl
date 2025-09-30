!start.

#nb_planets(12).

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!respond(DEST,INFO) <- .send(DEST, tell, INFO).

+!request_nb_planets[source(X)] : nb_planets(N) <-
    !respond(X,nb_planets(N)).

+!request_nb_planets[source(X)] : not nb_planets(_) <-
    .prompt(nb_planets);
    +respond_to(X).

+respond_to(X) <-
    .print("waiting for llm response.").

+nb_planets(X)[source(llm)] : respond_to(D) <-
    .print("response received from llm, going to respond to", D);
    -respond_to(D) ;
    !respond(D,nb_planets(X)).
