
from autogen_core import type_subscription, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, UserMessage, RequestUsage

import autogen_agentspeak.bdi
import agentspeak
import asyncio

import message


@type_subscription(topic_type=message.asp_message_rcv)
class ReceiverAgent(autogen_agentspeak.bdi.BDIAgent):

    async def run_prompt(self, subject: agentspeak.Literal, v:int):
        if str(subject) == "has_pattern_matching_for_instanceof" :
            prompt = "In Java version " + str(v) + ", is there pattern matching for instanceof? Answer with a single boolean True or False."
            llm_result = await self._model_client.create(
                messages=[
                    UserMessage(content=prompt, source=self.id.key),
                ],
                cancellation_token=None,
            )
            response = llm_result.content
            try:
                b= (response.startswith("True") or response.startswith("true"))
                s = ("" if b else "~") + "has_pattern_matching_for_instanceof(" + str(v) + ")"

                (functor, args) = autogen_agentspeak.bdi.parse_literal(s)
                m = agentspeak.Literal(functor, args)
                tagged_m = m.with_annotation(
                    agentspeak.Literal("source", (agentspeak.Literal("llm"),))
                    )
                self.asp_agent.call(agentspeak.Trigger.addition, agentspeak.GoalType.belief, tagged_m, agentspeak.runtime.Intention())
                self.env.run()

            except ValueError:
                print("bad result from llm: " + response)
        else:
            print("bad request: " + str(subject) + ".")

    def __init__(self, descr, model_client : ChatCompletionClient):
        super().__init__(descr, "llm_dealer.asl")
        self._model_client = model_client


    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        @actions.add_procedure(
                functor=".prompt",
                arg_specs=(
                   agentspeak.Literal,
                ),
            )
        def _prompt(subject: agentspeak.Literal):
            task = asyncio.create_task(self.run_prompt(subject.functor, subject.args[0]))


    @message_handler
    async def handle_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.on_receive(message, ctx)

