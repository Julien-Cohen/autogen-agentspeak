from ast import literal_eval

# from https://github.com/sfp932705/spade_bdi/blob/master/spade_bdi/bdi.py
def parse_literal(msg):
    functor = msg.split("(")[0]
    if "(" in msg:
        args = msg.split("(")[1]
        args = args.split(")")[0]
        args = literal_eval(args)

        def recursion(arg):
            if isinstance(arg, list):
                return tuple(recursion(i) for i in arg)
            return arg

        new_args = (recursion(args),)

    else:
        new_args = ''
    return functor, new_args