
from autogen_core import type_subscription, message_handler, MessageContext, TopicId, RoutedAgent

import message as message_module

# We import bdi because we need the message format that the AgentSpeak agents is expecting.
import autogen_agentspeak.bdi
from dataclasses import dataclass

@dataclass
class StartMessage:
    val="start"

@type_subscription(topic_type=message_module.asp_message_send)
class SenderAgent(RoutedAgent):

    @message_handler(strict=True)
    async def handle_asp_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        print("[" + self.id.key + "] Sender awake by message reception (AgentSpeakMessage).")

        if message.illocution == "tell" and message.content == "pong":
            print("[" + self.id.key + "] Pong received.")
        else:
            print("[" + self.id.key + "] This message could not be handled.")

    @message_handler(strict=True)
    async def handle_start_message(self, message : StartMessage, ctx: MessageContext) -> None:
        print("[" + self.id.key + "] Sender awake by message reception (StartMessage).")

        await self.tell(message_module.asp_message_rcv, "sender_alive", message_module.asp_message_send)

    async def tell(self, dest, lit, source):
        await self.publish_message(
            autogen_agentspeak.bdi.AgentSpeakMessage(
                illocution="tell",
                content=lit,
                sender=source
            ),
            topic_id=TopicId(dest, source="default"),
        )
        print("[" + self.id.key + "] tell sent.")






