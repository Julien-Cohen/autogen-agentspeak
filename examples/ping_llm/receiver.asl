!start.

+!start <-
    .print("hello from receiver").

+!request <-
    .prompt(hello, ANSWER);
    .wait(1000);
    .print("end of wait").


+nb_planets(X) <-
    .print("awake");
    .autogen_send(to_sender,tell,nb_planets(X),_).
