!start.

+!start <-
    .print("hello from receiver").

+!request <-
    .prompt(hello);
    +waiting.

+waiting <- .print("waiting for the response.").

-waiting <- .print("finished waiting.").

+nb_planets(X) : waiting <-
    -waiting ;
    .autogen_send(to_sender,tell,nb_planets(X)).
