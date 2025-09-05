import os
from ast import literal_eval

import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext

from message import MyMessage
import message as message_module



@type_subscription(topic_type=message_module.asp_message)
class ReceiverAgent(RoutedAgent):

    def __init__(self, descr):
        print("Building a new ReceiverAgent")
        super().__init__(descr)

        self.env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "receiver.asl")) as source:
            self.a=self.env.build_agent(source, agentspeak.stdlib.actions)

        self.env.run()

    @message_handler
    async def handle_message(self, message: MyMessage, ctx: MessageContext) -> None:
        print("(python layer) Message received. ")
        if message.illocution == "TELL":
            print ("TELL " + message.content)

            (functor, args) = parse_literal(message.content)
            m = agentspeak.Literal(functor, args)
            print (str(m))
            print("call")
            self.a.call(
                agentspeak.Trigger.addition,
                agentspeak.GoalType.belief,
                m,
                agentspeak.runtime.Intention())
            print("step")
            self.a.step()

            print("end'")
        else:
            print ("unrecognized illocution:" + message.illocution)

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