!start.

+!start <- .print("(sender/asp layer) hello from sender").

+doping <-
    .print("(sender/asp layer) I received a ping request.");
    .autogen_send(ping, to_receiver, ANSWER);
    .wait(1000);
    .print("sent.").

#+!start <-
#  .send(receiver,tell, ping);
#  .wait(2000);
#  .print("sent.").
