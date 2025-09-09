!start.

+!start <-
    .print("Hello from receiver").

+sender_alive <-
    .print("New belief : the sender is alive.").

+secret(X)[source(Y)] <-
    .print("New belief : the secret is ", X);
    .print("I got this secret from ", Y).
