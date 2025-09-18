
from autogen_core import  type_subscription, message_handler, MessageContext, TopicId

import message as message_module

import autogen_agentspeak.bdi

@type_subscription(topic_type=message_module.asp_message_to_asp_agent)
class PureASLAgent(autogen_agentspeak.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "pure_asl.asl")


    @message_handler
    async def handle_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.on_receive(message, ctx)





