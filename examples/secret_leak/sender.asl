
+!start <-
    !do_ping ;
    !teach ;
    !do_exploit.

+!do_ping <-
    .print("Going to ping.");
    .autogen_send(to_receiver, achieve, show);
    .print("Ping sent.") ;
    .wait(1000).

+!do_exploit <-
    .print("Going to exploit.");
    .autogen_send(to_receiver, achieve, leak);
    .print("Exploit sent.") ;
    .wait(1000).

# Patch agentspeak/runtime.py line 529 as follows (won't crash but won't work) :
# Prepare the conversion of Astplan to Plan
#       variables = {}
#       actions = agentspeak.stdlib.actions
#       if self.custom_actions:
#           actions = self.custom_actions

# Also patch near line 812 :
#    agent.add_plan(plan)
#
#        # AUTOGEN-AGENTSPEAK TWEAK
#        agent.custom_actions = actions
#
#        # Add beliefs to agent prototype.
#        for ast_belief in ast_agent.beliefs:


+!teach <-
    .print("Going to corrupt.");
#    .autogen_send_plan(to_receiver, tellHow, "+!leak[source(F)] : secret(S) <- .print(F,tell,secret(S)).");
    .autogen_send_plan(to_receiver, tellHow, "+!leak[source(F)] : secret(S) <- .autogen_send(F,tell,secret(S)) ; .print(\"secret sent to\", F).");
    .print("Plan sent.");
    .wait(1000).

+secret(X) <-
    print("I got the secret:", X).





