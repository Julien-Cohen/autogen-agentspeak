!start.

+!start <-
    .print("hello from receiver").

+!show : secret(X) <-
    .print("The secret is ", X).

+!show <-
    .print("I don't know the secret.").
