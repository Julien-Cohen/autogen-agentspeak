def remove_brackets(s):
    return s.removeprefix("[").removesuffix("]")

def split_on_pipe(s):
    if "|" in s:
        (b, _, a) = s.partition("|")
        return (b, a)
    else:
        raise ValueError("No pipe in this string.")


def filter_quotes(s:str):
    return s.replace("\"", "\\\"")

def custom_print_list(l):
    for s in l :
        print(" * " + s)

def parse_bool(s):
            if s.startswith("True") or s.startswith("true"):
                return True
            elif s.startswith("False") or s.startswith("false"):
                return False
            else:
                return None