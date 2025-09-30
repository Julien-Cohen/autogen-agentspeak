!start.

+!start <-
    .my_name(N) ;
    .print("hello from", N).

+!respond(DEST,INFO) <- .send(DEST, tell, INFO).

+!request_has_pattern_matching_for_instanceof(V)[source(X)] : has_pattern_matching_for_instanceof(V) <-
    !respond(X,has_pattern_matching_for_instanceof(V)).

+!request_has_pattern_matching_for_instanceof(V)[source(X)] : ~has_pattern_matching_for_instanceof(V) <-
    !respond(X,~has_pattern_matching_for_instanceof(V)).

+!request_has_pattern_matching_for_instanceof(V)[source(X)] : not has_pattern_matching_for_instanceof(V) <-
    .prompt(has_pattern_matching_for_instanceof(V));
    +respond_to(X).

+respond_to(X) <-
    .print("waiting for llm response.").

+has_pattern_matching_for_instanceof(V) : respond_to(D) <-
    .print("response received from llm, going to respond to", D);
    -respond_to(D) ;
    !respond(D,has_pattern_matching_for_instanceof(V)).

+~has_pattern_matching_for_instanceof(V) : respond_to(D) <-
    .print("response received from llm, going to respond to", D);
    -respond_to(D) ;
    !respond(D,~has_pattern_matching_for_instanceof(V)).