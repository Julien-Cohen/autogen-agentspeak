!start.

+!start <-
    .print("hello from sender").

+!do_ping <-
    .print("I received a ping request.");
    .send(to_receiver, achieve, say("Hello"));
    .wait(1000);
    .print("Sent.").


