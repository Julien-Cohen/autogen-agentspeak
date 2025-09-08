import os

import agentspeak.runtime
import agentspeak.stdlib as agentspeak_stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext, TopicId

import message as message_module

import asyncio

import agentspeak_autogen.bdi


@type_subscription(topic_type=message_module.asp_message_send)
class SenderAgent(agentspeak_autogen.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "sender.asl")


    @message_handler
    async def handle_message(self, message: agentspeak_autogen.bdi.MyMessage, ctx: MessageContext) -> None:
        self.on_receive(message)





