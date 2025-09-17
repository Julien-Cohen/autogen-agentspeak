
from autogen_core import type_subscription, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, UserMessage

import autogen_agentspeak.bdi
import autogen_agentspeak.talk_to_bdi
import asyncio

import message as message_module
from examples.llm_translation.message import asp_message_to_asp_agent, asp_message_to_translator


@type_subscription(topic_type=message_module.asp_message_to_translator)
class TranslatorAgent(autogen_agentspeak.talk_to_bdi.BDITalker):

    async def translate(self, text, ctx):

            prompt = ("Your task is to translate a human request into an AgentSpeak goals for a robot."
                        + " The possible AgentSpeak achievements are do_move to move and do_jump to jump. "
                        + " Here is the sentence to translate. [BEGIN] "
                      + text + "[END] "
                      + "Respond with only one achievement."
                      )
            llm_result = await self._model_client.create(
                messages=[
                    UserMessage(content=prompt, source=self.id.key),
                ],
                cancellation_token=None,
            )
            response = llm_result.content
            print ("response = " + str(response))

            # refactor-me : achieve
            await self.achieve(asp_message_to_asp_agent, response, asp_message_to_translator)


    def __init__(self, descr, model_client : ChatCompletionClient):
        super().__init__(descr)
        self._model_client = model_client


    @message_handler
    async def handle_message(self, message: message_module.HumanMessage, ctx: MessageContext) -> None:
        await self.translate(message.human_content, ctx)

