from autogen_core import type_subscription, message_handler, MessageContext, TopicId, RoutedAgent
from autogen_core.models import ChatCompletionClient, UserMessage

import autogen_agentspeak.bdi
import utils
import autogen_agentspeak.utils as aa_utils

import message as message_module
from autogen_agentspeak.talk_to_bdi import BDITalker


@type_subscription(topic_type=message_module.asp_message_to_completeness_evaluator)
class CompletenessEvaluatorAgent(BDITalker):

    async def run_prompt(self, spec:str, req:str):
        prompt = "Evaluate if the following list of requirements covers the function's specification input, output, and behavior \"" + spec + "\":" + req + ". Answer only with \"True\" or \"False\" (mind the case)."
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
    async def handle_asp_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.log("Completeness evaluator awake by message reception (AgentSpeakMessage).")

        if message.illocution == "tell" and message.content.startswith("spec"):
            self.log("Specification received. " + str(message.content))
            self.spec = utils.isolate_spec_from_literal(str(message.content))
            self.log("Spec received: " + self.spec)

        elif message.illocution == "tell" and message.content.startswith("req"):
            self.log("Requirements received. " + str(message.content))
            self.list_req = utils.extract_list_from_req_lit(message.content)
            self.str_req = ' ; '.join([str(s) for s in self.list_req])
            self.log(str(len(self.list_req)) + " requirements received. " )

        elif message.illocution == "achieve" and message.content == "evaluate":
            self.log("Request to evaluate.")
            if len(self.list_req) == 0:
                self.log("Empty list.")
                response = "False"
            else:
                response = await self.run_prompt(self.spec, self.str_req)
            self.log("Response: " + response)
            await self.tell(message_module.asp_message_to_manager, "completeness(" + aa_utils.filter_quotes(str(response)) + ")", message_module.asp_message_to_completeness_evaluator)
        else:
            self.log("This message could not be handled.")
