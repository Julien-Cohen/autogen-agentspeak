!start.

# java_version(5).
# java_version(11).
 java_version(21).

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!do_request : java_version(X) <-
    .print("I received a request.");
    .print("Considering Java", X) ;
    .autogen_send(llm_dealer, achieve, request_has_pattern_matching_for_instanceof(X)).

+has_pattern_matching_for_instanceof(X): java_version(X) <-
    .print("Ok, we can use pattern matching with instanceof.").

+~has_pattern_matching_for_instanceof(X): java_version(X) <-
    .print("Warning: we CANNOT use pattern matching with instanceof.").