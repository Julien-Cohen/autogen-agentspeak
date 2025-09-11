!start.

+!start <-
    .print("hello from receiver").

+!request <-
    .prompt(hello, ANSWER).

+nb_planets(X) <-
    .autogen_send(to_sender,tell,nb_planets(X),_).
