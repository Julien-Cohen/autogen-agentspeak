!start.

+!start <- .print("(sender/asp layer) hello from sender").

+!doping <-
    .print("(sender/asp layer) I received a ping request.").

#+!start <-
#  .send(receiver,tell, ping);
#  .wait(2000);
#  .print("sent.").
