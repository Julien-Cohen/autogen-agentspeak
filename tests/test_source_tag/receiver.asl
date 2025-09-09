!start.

+!start <-
    .print("Hello from receiver").

+secret(X)[source(Y)] <-
    .print("New belief : the secret is ", X);
    .print("I got this secret from ", Y).
