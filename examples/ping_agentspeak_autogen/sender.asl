!start.

+!start <- .print("(sender/asp layer) hello from sender").

+doping <-
    .print("(sender/asp layer) I received a ping request.");
    .autogen_send(ping, ANSWER);
    .wait(2000);
    .print("sent.").

#+!start <-
#  .send(receiver,tell, ping);
#  .wait(2000);
#  .print("sent.").
