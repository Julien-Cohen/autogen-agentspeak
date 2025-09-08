import os
from ast import literal_eval

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent


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

class BDIAgent(RoutedAgent):

    def __init__(self, descr, asl_file):
        super().__init__(descr)

        self.env = agentspeak.runtime.Environment()

        # add custom actions (must occur before loading the asl file)
        self.bdi_actions = agentspeak.Actions(agentspeak.stdlib.actions)
        self.add_custom_actions(self.bdi_actions)

        with open(asl_file) as source:
            self.a=self.env.build_agent(source, self.bdi_actions)

        self.env.run()

    # abstract method
    def add_custom_actions(self, actions):
        pass