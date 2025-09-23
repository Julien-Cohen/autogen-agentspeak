
from autogen_core import type_subscription, message_handler, MessageContext

import autogen_agentspeak.bdi

@type_subscription(topic_type="to_receiver")
class ReceiverAgent(autogen_agentspeak.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "receiver.asl")

    @message_handler
    async def handle_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.on_receive(message, ctx)

