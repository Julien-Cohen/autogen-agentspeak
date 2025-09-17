from autogen_core import RoutedAgent, TopicId
import autogen_agentspeak.bdi

class BDITalker(RoutedAgent):
    """ Services to talk with BDI (AgentSpeak) agents (class AgentSpeakAgent) """

    def log(self, s):
        print("[" + self.id.type + "] " + s)


    async def send(self, illocution:str, dest: str, lit: str, source):
        await self.publish_message(
            autogen_agentspeak.bdi.AgentSpeakMessage(
                illocution=illocution,
                content=lit,
                sender=source
            ),
            topic_id=TopicId(dest, source="default"),
        )
        self.log(illocution + " sent.")

    async def tell(self, dest: str, lit: str, source):
        await self.send("tell", dest, lit,source)


    async def achieve(self, dest: str, lit: str, source):
       await self.send("achieve", dest, lit,source)
