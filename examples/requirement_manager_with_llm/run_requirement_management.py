#!/usr/bin/env python

import context
import asyncio

from autogen_core import SingleThreadedAgentRuntime, TopicId, RoutedAgent, type_subscription, message_handler, \
    MessageContext
from autogen_ext.models.openai import OpenAIChatCompletionClient

import message
from autogen_agentspeak.talk_to_bdi import BDITalker
from examples.requirement_manager_with_llm.message import asp_message_to_driver
from manager import ManagerAgent
from completeness_evaluator import CompletenessEvaluatorAgent
from generator import GeneratorAgent
import autogen_agentspeak
import utils
import autogen_agentspeak.utils as aa_utils

@type_subscription(topic_type=asp_message_to_driver)
class DriverAgent(BDITalker):

    @message_handler(strict=True)
    async def handle_asp_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.log("Driver awake by message reception (AgentSpeakMessage).")

        if message.illocution == "tell" and message.content.startswith("req"):
            self.log("Requirements received.")
            self.l = utils.extract_list_from_req_lit(message.content)
            aa_utils.custom_print_list(self.l)

        else:
            self.log("This message could not be handled.")



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
        factory=lambda: CompletenessEvaluatorAgent("test completeness evaluator agent", model_client=model_client),
    )

    await GeneratorAgent.register(
        autogen_runtime,
        type=message.asp_message_to_generator,
        factory=lambda: GeneratorAgent("test generator agent", model_client=model_client),
    )

    await DriverAgent.register(
        autogen_runtime,
        type=message.asp_message_to_driver,
        factory=lambda: DriverAgent("test driver agent"),
    )

    # Start AutoGen runtime
    autogen_runtime.start()

    example_spec="A function to compare two words."

    # Send a first message to give the spec
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.AgentSpeakMessage(
            illocution="tell",
            content="spec(\"" + example_spec + "\")", # fixme : automate build literal
            sender=asp_message_to_driver
        ),
        topic_id=TopicId(message.asp_message_to_manager, source="default"),
    )

    # Send a second message to trigger behavior
    await autogen_runtime.publish_message(
        autogen_agentspeak.bdi.AgentSpeakMessage(
            illocution="achieve",
            content="build",
            sender=asp_message_to_driver
        ),
        topic_id=TopicId(message.asp_message_to_manager, source="default"),
    )

    await autogen_runtime.stop_when_idle()


asyncio.run(main())