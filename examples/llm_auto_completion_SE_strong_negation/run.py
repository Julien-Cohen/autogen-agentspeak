#!/usr/bin/env python
import context
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId

import message
from llm_dealer import LLMDealerAgent
from manager import ManagerAgent

import autogen_agentspeak.bdi

# pip install "autogen-ext[openai]"
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
        )

    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    # Register AutoGen agents types
    # (AutoGen creates agents only when needed for message delivery.)
    await LLMDealerAgent.register(
        autogen_runtime,
        type=message.asp_message_dealer,
        factory=lambda: LLMDealerAgent("test receiver agent", model_client=model_client),
    )

    await ManagerAgent.register(
        autogen_runtime,
        type=message.asp_message_manager,
        factory=lambda: ManagerAgent("test sender agent"),
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
        topic_id=TopicId(message.asp_message_manager, source="default"),
    )

    await asyncio.sleep(5) # otherwise, autogen stops before an answer from the LLM is received.
    await autogen_runtime.stop_when_idle()
    await model_client.close()


asyncio.run(main())