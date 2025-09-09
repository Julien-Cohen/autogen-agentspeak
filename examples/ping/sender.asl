!start.

+!start <- .print("(sender/asp layer) hello from sender").

+!do_ping <-
    .print("(sender/asp layer) I received a ping request.");
    .autogen_send(to_receiver, tell, sender_alive, ANSWER);
    .wait(1000);
    .print("(sender/asp layer) sent.").

