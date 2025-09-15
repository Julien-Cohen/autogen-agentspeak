from autogen_core import RoutedAgent, TopicId
import autogen_agentspeak.bdi

class BDITalker(RoutedAgent):
    """ Services to talk with BDI (AgentSpeak) agents (class AgentSpeakAgent) """

    def log(self, s):
        print("[" + self.id.type + "] " + s)


    async def tell(self, dest: str, lit: str, source):
        await self.publish_message(
            autogen_agentspeak.bdi.AgentSpeakMessage(
                illocution="tell",
                content=lit,
                sender=source
            ),
            topic_id=TopicId(dest, source="default"),
        )
        self.log("tell sent.")
