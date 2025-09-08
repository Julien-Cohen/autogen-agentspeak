import os


import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext

from message import MyMessage
import message as message_module

import agentspeak_autogen.bdi


@type_subscription(topic_type=message_module.asp_message_rcv)
class ReceiverAgent(RoutedAgent):

    def __init__(self, descr):
        super().__init__(descr)

        self.env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "receiver.asl")) as source:
            self.a=self.env.build_agent(source, agentspeak.stdlib.actions)

        self.env.run()

    @message_handler
    async def handle_message(self, message: MyMessage, ctx: MessageContext) -> None:
        if message.illocution == "TELL":

            (functor, args) = agentspeak_autogen.bdi.parse_literal(message.content)
            m = agentspeak.Literal(functor, args)
            self.a.call(
                agentspeak.Trigger.addition,
                agentspeak.GoalType.belief,
                m,
                agentspeak.runtime.Intention())
            self.env.run()

        else:
            print ("unrecognized illocution:" + message.illocution)
