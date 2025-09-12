
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
    async def handle__start_message(self, message : StartMessage, ctx: MessageContext) -> None:
        print("[" + self.id.key + "] Sender awake by message reception (StartMessage).")

        await self.publish_message(
                    autogen_agentspeak.bdi.AgentSpeakMessage(
                        illocution = "tell",
                        content    = "sender_alive",
                        sender     = message_module.asp_message_send
                    ),
                    topic_id=TopicId(message_module.asp_message_rcv, source="default"),
                )
        print("[" + self.id.key + "] Ping sent.")






