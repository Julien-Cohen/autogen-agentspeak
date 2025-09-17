
from autogen_core import type_subscription, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, UserMessage

import autogen_agentspeak.bdi
import autogen_agentspeak.talk_to_bdi
import asyncio

import message as message_module
from autogen_agentspeak.talk_to_bdi import extract_catalog
from examples.llm_translation.message import asp_message_to_asp_agent, asp_message_to_translator


@type_subscription(topic_type=message_module.asp_message_to_translator)
class TranslatorAgent(autogen_agentspeak.talk_to_bdi.BDITalker):

    async def translate(self, text: str, achievements, ctx):
            catalog = extract_catalog(achievements)
            self.log("Translator agent received the following request: " + text)

            prompt = ("Your task is to translate a human request into an AgentSpeak goals for a robot."
                        + " The possible AgentSpeak achievements are described in the following list. [BEGIN LIST OF ACHIEVEMENTS] "
                        + catalog
                        + "[END OF LIST OF ACHIEVEMENTS]"
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
            self.log ("LLM response = " + str(response))

            # refactor-me : achieve
            await self.achieve(asp_message_to_asp_agent, response, asp_message_to_translator)


    def __init__(self, descr, model_client : ChatCompletionClient):
        super().__init__(descr)
        self._model_client = model_client
        self.achievement_catalog = None


    @message_handler
    async def handle_human_message(self, message: message_module.HumanMessage, ctx: MessageContext) -> None:
        self.log("Human query received.")
        tentatives = 10
        while tentatives >0 and not self.achievement_catalog :
            print("Catalog of achievement has not been initialized. Trying again soon.")
            await asyncio.sleep(2)
            tentatives = tentatives - 1
        if not self.achievement_catalog :
            print ("Catalog of achievement has not been initialized. Stopping.")
        else:
            await self.translate(message.human_content, self.achievement_catalog, ctx)

    @message_handler
    async def handle_command_message(self, message: message_module.Command, ctx: MessageContext) -> None:
        self.log("Command Message received")
        await self.achieve(message_module.asp_message_to_asp_agent, "publish", message_module.asp_message_to_translator)

    @message_handler
    async def handle_asp_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.log("ASP message received")
        if message.illocution == "tell" and message.content.startswith("catalog("):
            self.achievement_catalog = autogen_agentspeak.talk_to_bdi.extract_catalog(message.content)
            self.log("Catalog of achievement initialized: " + self.achievement_catalog)


