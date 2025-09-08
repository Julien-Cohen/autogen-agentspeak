import os


import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext

from message import MyMessage
import message as message_module

import agentspeak_autogen.bdi


@type_subscription(topic_type=message_module.asp_message_rcv)
class ReceiverAgent(agentspeak_autogen.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "receiver.asl")


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
