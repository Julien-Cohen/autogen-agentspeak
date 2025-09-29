!start.

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!do_ping <-
    .print("I received a ping request.");
    .send(to_receiver, achieve, do_jump).

