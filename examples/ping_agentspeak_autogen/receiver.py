import os


import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext


import message as message_module

import agentspeak_autogen.bdi


@type_subscription(topic_type=message_module.asp_message_rcv)
class ReceiverAgent(agentspeak_autogen.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "receiver.asl")


    @message_handler
    async def handle_message(self, message: agentspeak_autogen.bdi.MyMessage, ctx: MessageContext) -> None:
        self.on_receive(message)

