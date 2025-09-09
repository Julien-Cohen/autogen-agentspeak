#!/usr/bin/env python

import os
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId

import message
from receiver import ReceiverAgent
from sender import SenderAgent

import autogen_agentspeak.bdi

async def main():
    # AgentSpeak init : we don't init the agentspeakruntime here.
    # It is initialized in each agent.
    # agentspeak_env = agentspeak.runtime.Environment()

    #with open(os.path.join(os.path.dirname(__file__), "sender.asl")) as source:
    #    agentspeak_env.build_agent(source, agentspeak.stdlib.actions)

    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    # Create AutoGen agents
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

    # We don't run any agentspeak runtime here.
    # They are run by each agent.
    # agentspeak_env.run()

    # Start AutoGen runtime
    autogen_runtime.start()

    # Send a message
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.MyMessage(
            illocution="TELL",
            content="do_ping",
        ),
        topic_id=TopicId(message.asp_message_send, source="default"),
    )


    await autogen_runtime.stop_when_idle()


asyncio.run(main())