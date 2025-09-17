#!/usr/bin/env python
import context
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId

import message
from llm_translator import TranslatorAgent
from pure_asl import PureASLAgent

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
    await TranslatorAgent.register(
        autogen_runtime,
        type=message.asp_message_to_translator,
        factory=lambda: TranslatorAgent("test translator agent", model_client=model_client),
    )

    await PureASLAgent.register(
        autogen_runtime,
        type=message.asp_message_to_asp_agent,
        factory=lambda: PureASLAgent("test asl agent"),
    )

    # Start AutoGen runtime
    autogen_runtime.start()

    # Send a first message to init the first agent
    await autogen_runtime.publish_message(
        message.Command(
            content="..."
        ),
        topic_id=TopicId(message.asp_message_to_translator, source="default"),
    )

    await asyncio.sleep(2)

    # Send a message to trigger agent behavior
    await autogen_runtime.publish_message(
        message.HumanMessage(
            human_content="Please move dear robot."
        ),
        topic_id=TopicId(message.asp_message_to_translator, source="default"),
    )

    await asyncio.sleep(2)

    # Send a second message to trigger agent behavior
    await autogen_runtime.publish_message(
        message.HumanMessage(
            human_content="Please jump now."
        ),
        topic_id=TopicId(message.asp_message_to_translator, source="default"),
    )

    print ("second order sent")

    print("WARNING: because of asynchronous calls to the LLM, the jump and move orders can arrive at the robot agent in any order.")

    await asyncio.sleep(5) # otherwise, autogen stops before an answer from the LLM is received.
    await autogen_runtime.stop_when_idle()
    await model_client.close()


asyncio.run(main())