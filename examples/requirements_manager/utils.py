
def isolate_spec_from_literal(s):
    tmp1=s.removeprefix("spec(")
    tmp2=tmp1.removesuffix(")")
    return tmp2

def isolate_list(s):
    """Returns the list string in a string representing a requirement list, such as req(a,b,c)"""
    tmp1=s.removeprefix("req(")
    tmp2=tmp1.removesuffix(")")
    return tmp2

def extract_list_from_req_lit(s):
    s2 = isolate_list(s)
    if s2 == "[]":
        return []
    else :
        tmp1 = s2.removeprefix("[") # remove everything before [
        tmp2 = tmp1.removesuffix("]")
        t = tmp2.split("|")
        for i in range(len(t)):
            t[i] = t[i].removeprefix("\"")
            t[i] = t[i].removesuffix("\"")
        return t

def filter_quotes(s:str):
    return s.replace("\"", "\\\"")
