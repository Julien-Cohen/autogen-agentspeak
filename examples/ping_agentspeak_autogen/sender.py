import os

import agentspeak.runtime
import agentspeak.stdlib as agentspeak_stdlib
from autogen_core import RoutedAgent, type_subscription, message_handler, MessageContext, TopicId

from message import MyMessage
import message as message_module

import asyncio

import agentspeak_autogen.bdi


@type_subscription(topic_type=message_module.asp_message_send)
class SenderAgent(agentspeak_autogen.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "sender.asl")


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
                MyMessage(
                    illocution="TELL",
                    content="ping",
                ),
                topic_id=TopicId(message_module.asp_message_rcv, source="default"),
            ))



