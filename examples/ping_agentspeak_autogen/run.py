#!/usr/bin/env python

import os
import asyncio

import agentspeak.runtime
import agentspeak.stdlib

from autogen_core import SingleThreadedAgentRuntime, TopicId

from message import MyMessage
import message
from receiver import ReceiverAgent

async def main():
    # AgentSpeak init
    #agentspeak_env = agentspeak.runtime.Environment()

    #with open(os.path.join(os.path.dirname(__file__), "sender.asl")) as source:
    #    agentspeak_env.build_agent(source, agentspeak.stdlib.actions)

    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    await ReceiverAgent.register(
        autogen_runtime,
        type=message.asp_message,
        factory=lambda: ReceiverAgent("test agent"),
    )

    #agentspeak_env.run()

    autogen_runtime.start()

    await autogen_runtime.publish_message(
        MyMessage(
            illocution="TELL",
            content="ping",
        ),
        topic_id=TopicId(message.asp_message, source="default"),
    )

    await autogen_runtime.stop_when_idle()


asyncio.run(main())