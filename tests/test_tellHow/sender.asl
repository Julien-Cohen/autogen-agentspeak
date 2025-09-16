
+!start <-
    !do_ping ;
    !teach ;
    !do_ping_alt.

+!do_ping <-
    .print("Going to ping.");
    .autogen_send(to_receiver, achieve, show);
    .print("Ping sent.") ;
    .wait(1000).

+!do_ping_alt <-
    .print("Going to ping_alt.");
    .autogen_send(to_receiver, achieve, show_alt);
    .print("Ping_alt sent.") ;
    .wait(1000).

+!teach <-
    .print("Going to teach.");
    .autogen_send_plan(to_receiver, tellHow, "+!show_alt <- .my_name(N) ; .print(\"hello from\",N).");
    .print("Plan sent.");
    .wait(1000).


