import autogen_agentspeak.utils as aa_utils

def isolate_spec_from_literal(s):
    tmp1=s.removeprefix("spec(")
    tmp2=tmp1.removesuffix(")")
    return tmp2

def isolate_list(s):
    """Returns the list string in a string representing a requirement list, such as req(a,b,c)"""
    tmp1=s.removeprefix("req(")
    tmp2=tmp1.removesuffix(")")
    return tmp2




def remove_quotes_opt(s):
    if s.startswith("\"") and s.endswith("\""):
        return s.removeprefix("\"").removesuffix("\"")
    elif s.startwith("\"") or s.endswith("\""):
            raise ValueError ("Inconsistent quotes.")
    else:
        return s

def extract_list_from_req_lit(s):
    """Convert nested lists encoded in strings into plain python lists.

    Recursive function.

    Example: '["abc"|[]]' is converted into ["abc"]
    """

    s2 = isolate_list(s)
    if s2 == "[]":
        return []
    else :
        tmp2 = aa_utils.remove_brackets(s2)
        (e,r) = aa_utils.split_on_pipe(tmp2)
        e2 = remove_quotes_opt(e)
        r2 = extract_list_from_req_lit(r) # recursion
        r2.insert(0,e2)
        return r2


def run_test():
    r = extract_list_from_req_lit('["abc"|[]]')
    print(str(r))
    print (len(r))
    print (len(r)==1)

#run_test()
