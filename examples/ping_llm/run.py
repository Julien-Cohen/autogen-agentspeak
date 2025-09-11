#!/usr/bin/env python

import os
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId

import message
from receiver import ReceiverAgent
from sender import SenderAgent

import autogen_agentspeak.bdi

# pip install "autogen-ext[openai]"
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            # api_key="YOUR_API_KEY"
        )
    
    
    
    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    # Register AutoGen agents types
    # (AutoGen creates agents only when needed for message delivery.)
    await ReceiverAgent.register(
        autogen_runtime,
        type=message.asp_message_rcv,
        factory=lambda: ReceiverAgent("test receiver agent", model_client=model_client),
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
        autogen_agentspeak.bdi.AgentSpeakMessage(
            illocution="achieve",
            content="do_request",
            sender = "main"
        ),
        topic_id=TopicId(message.asp_message_send, source="default"),
    )

    await asyncio.sleep(10) # otherwise, autogen stops before an answer from the LLM is received.
    await autogen_runtime.stop_when_idle()
    await model_client.close()


asyncio.run(main())