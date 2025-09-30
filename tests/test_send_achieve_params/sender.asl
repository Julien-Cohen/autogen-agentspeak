!start.

+!start <-
    .print("hello from sender").

+!do_ping <-
    .print("I received a ping request.");
    .send(to_receiver, achieve, say("Hello", "World"));
    .wait(1000);
    .print("Sent.").

# FIXME : the following does not work
# say(true)
# say(True)
# say(blue)


