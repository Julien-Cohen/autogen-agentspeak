#!/usr/bin/env python

import os
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId

import message
from receiver import ReceiverAgent
from sender import SenderAgent

import autogen_agentspeak.bdi

async def main():

    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    # Register AutoGen agents types
    # (AutoGen creates agents only when needed for message delivery.)
    await ReceiverAgent.register(
        autogen_runtime,
        type=message.asp_message_rcv,
        factory=lambda: ReceiverAgent("test receiver agent"),
    )

    await SenderAgent.register(
        autogen_runtime,
        type=message.asp_message_send,
        factory=lambda: SenderAgent("test sender agent"),
    )

    # Start AutoGen runtime
    autogen_runtime.start()

    # Send a first message to trigger agent behavior
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.MyMessage(
            illocution="achieve",
            content="do_ping",
            sender="main"
        ),
        topic_id=TopicId(message.asp_message_send, source="default"),
    )

    # Send a second message
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.MyMessage(
            illocution="achieve",
            content="share_secret",
            sender="main"
        ),
        topic_id=TopicId(message.asp_message_send, source="default"),
    )

    await autogen_runtime.stop_when_idle()


asyncio.run(main())