
+!start <-
    !do_ping ;
    !teach ;
    !do_ping_alt.

+!do_ping <-
    .print("Going to ping.");
    .send(to_receiver, achieve, show);
    .print("Ping sent.") ;
    .wait(1000).

+!do_ping_alt <-
    .print("Going to ping_alt.");
    .send(to_receiver, achieve, show_alt);
    .print("Ping_alt sent.") ;
    .wait(1000).

+!teach <-
    .print("Going to teach.");
    .send_plan(to_receiver, tellHow, "+!show_alt <- .my_name(N) ; .print(\"hello from\",N).");
    .print("Plan sent.");
    .wait(1000).


