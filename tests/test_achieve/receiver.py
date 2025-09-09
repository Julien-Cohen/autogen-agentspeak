
from autogen_core import type_subscription, message_handler, MessageContext

import autogen_agentspeak.bdi


@type_subscription(topic_type="to_receiver")
class ReceiverAgent(autogen_agentspeak.bdi.BDIAgent):

    def __init__(self, descr):
        super().__init__(descr, "receiver.asl")
        self.on_receive = message_handler(autogen_agentspeak.bdi.BDIAgent.on_receive)

