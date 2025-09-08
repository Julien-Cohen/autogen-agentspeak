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


    # this method is called by __init__
    def add_custom_actions(self, actions):

        # custom action
        @actions.add_function(
            ".autogen_send",
            (
                agentspeak.Literal,
            ),
        )
        def _autogen_send(lit):

            # (self.publish_message is defined with the async keyword)
            asyncio.create_task(self.publish_message(
                agentspeak_autogen.bdi.MyMessage(
                    illocution="TELL",
                    content="ping", #FIXME
                ),
                topic_id=TopicId(message_module.asp_message_rcv, source="default"),
            ))



