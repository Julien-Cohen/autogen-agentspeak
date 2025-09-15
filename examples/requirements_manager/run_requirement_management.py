#!/usr/bin/env python

import os
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId
from autogen_ext.models.openai import OpenAIChatCompletionClient

import message
from manager import ManagerAgent
from completeness_evaluator import CompletenessEvaluatorAgent
from generator import GeneratorAgent
import autogen_agentspeak

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    )

    # AutoGen init
    autogen_runtime = SingleThreadedAgentRuntime()

    # Register AutoGen agents types
    # (AutoGen creates agents only when needed for message delivery.)
    await ManagerAgent.register(
        autogen_runtime,
        type=message.asp_message_to_manager,
        factory=lambda: ManagerAgent("test receiver agent"),
    )

    await CompletenessEvaluatorAgent.register(
        autogen_runtime,
        type=message.asp_message_to_completeness_evaluator,
        factory=lambda: CompletenessEvaluatorAgent("test completeness evaluator agent"),
    )

    await GeneratorAgent.register(
        autogen_runtime,
        type=message.asp_message_to_generator,
        factory=lambda: GeneratorAgent("test generator agent", model_client=model_client),
    )

    # Start AutoGen runtime
    autogen_runtime.start()

    example_spec="A function to compare two words."

    # Send a first message to give the spec
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.AgentSpeakMessage(
            illocution="tell",
            content="spec(\"" + example_spec + "\")", # fixme : automate build literal
            sender="main"
        ),
        topic_id=TopicId(message.asp_message_to_manager, source="default"),
    )

    # Send a second message to trigger behavior
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.AgentSpeakMessage(
            illocution="achieve",
            content="build",
            sender="main"
        ),
        topic_id=TopicId(message.asp_message_to_manager, source="default"),
    )

    await autogen_runtime.stop_when_idle()


asyncio.run(main())