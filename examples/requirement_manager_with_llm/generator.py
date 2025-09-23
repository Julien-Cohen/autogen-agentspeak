
from autogen_core import type_subscription, message_handler, MessageContext, TopicId, RoutedAgent
from autogen_core.models import ChatCompletionClient, UserMessage

import autogen_agentspeak.bdi
import utils
import autogen_agentspeak.utils as aa_utils

import message as message_module
from autogen_agentspeak.talk_to_bdi import BDITalker


@type_subscription(topic_type=message_module.asp_message_to_generator)
class GeneratorAgent(BDITalker):

    async def run_prompt(self, spec:str, req):
        prompt = "Give-me an atomic requirement for the following specification:" + spec + "Answer with only the requirement."
        llm_result = await self._model_client.create(
            messages=[
                    UserMessage(content=prompt, source=self.id.key),
                ],
            cancellation_token=None,
            )
        self.log("Prompt sent and response received.")
        response = llm_result.content
        return response

    def __init__(self, descr, model_client : ChatCompletionClient):
        super().__init__(descr)
        self._model_client = model_client


    @message_handler
    async def handle_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.log("Requirement generator awake by message reception (AgentSpeakMessage).")

        if message.illocution == "tell" and message.content.startswith("spec"):
            self.log("Specification received. " + str(message.content))
            self.spec = utils.isolate_spec_from_literal(str(message.content))
            self.log("Spec received: " + self.spec)

        elif message.illocution == "tell" and message.content.startswith("req"):
            self.log("List of requirements received, as a literal= " + message.content)
            tmp = utils.extract_list_from_req_lit(message.content)
            print("Extraction as a list (len "+ str(len(tmp)) +"): " + str(tmp))
            self.l = tmp
            self.log(str(len(self.l)) + " requirements received. " + str(self.l))

        elif message.illocution == "achieve" and message.content == "generate":
            self.log("Request to generate.")
            response = await self.run_prompt(self.spec, ctx)
            self.log("Response: " + response)
            await self.tell(message_module.asp_message_to_manager, "new_req(\"" + aa_utils.filter_quotes(str(response)) + "\")",
                            message_module.asp_message_to_generator)
        else:
            self.log("This message could not be handled: "+ str(message))



