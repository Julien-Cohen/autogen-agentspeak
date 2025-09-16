
from autogen_core import type_subscription, message_handler, MessageContext, TopicId, RoutedAgent

import message as message_module

# We import bdi because we need the message format that the AgentSpeak agents is expecting.
import autogen_agentspeak.bdi
import utils
from autogen_agentspeak.talk_to_bdi import BDITalker


@type_subscription(topic_type=message_module.asp_message_to_completeness_evaluator)
class CompletenessEvaluatorAgent(BDITalker):


    @message_handler(strict=True)
    async def handle_asp_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.log("Completeness evaluator awake by message reception (AgentSpeakMessage).")

        if message.illocution == "tell" and message.content.startswith("req"):
            self.log("Requirements received. " + str(message.content))
            self.l = utils.extract_list_from_req_lit(message.content)
            self.log(str(len(self.l)) + " requirements received. " + str(self.l))
            utils.custom_print_list(self.l)

        elif message.illocution == "achieve" and message.content == "evaluate":
            self.log("Request to evaluate.")
            result= len(self.l)>2
            await self.tell(message_module.asp_message_to_manager, "completeness(" + str(result) + ")", message_module.asp_message_to_completeness_evaluator)
        else:
            self.log("This message could not be handled.")







