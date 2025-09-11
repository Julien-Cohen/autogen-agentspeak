
from autogen_core import type_subscription, message_handler, MessageContext, TopicId
from autogen_core.models import ChatCompletionClient, UserMessage, RequestUsage

import autogen_agentspeak.bdi
import agentspeak
import asyncio


@type_subscription(topic_type="to_receiver")
class ReceiverAgent(autogen_agentspeak.bdi.BDIAgent):

    async def truc(self):
        prompt = "How many planets are there in our solar system? Answer with a single number"
        print("creating a request")
        llm_result = await self._model_client.create(
            messages=[
                UserMessage(content=prompt, source=self.id.key),

            ],
            cancellation_token=None,
        )
        print ("received an answer")
        response = llm_result.content
        print(response)
        assert isinstance(response, str)
        try:
            v=int(response)
            s = "nb_planets(" + str(v) + ")"
            #self.asp_agent.add_belief(term=s, scope=None)
            (functor, args) = autogen_agentspeak.bdi.parse_literal(s)

            m = agentspeak.Literal(functor, args)

            self.asp_agent.call(agentspeak.Trigger.addition, agentspeak.GoalType.belief, m, agentspeak.runtime.Intention())
            self.env.run()
            print("new belief added :" + str(agentspeak.Literal(s)))
        except ValueError:
            print("bad result from llm")

    def __init__(self, descr, model_client : ChatCompletionClient):


        super().__init__(descr, "receiver.asl")
        self._model_client = model_client


    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)


        @actions.add_function(
                ".prompt",
                (
                   agentspeak.Literal,

                ),
            )
        def _prompt(content):
            task = asyncio.create_task(self.truc())
            # set().add(task) # add a strong reference FIXME
            # La tâche est crée mais elle n'est pas allouée avant la fin du programme



    @message_handler
    async def handle_message(self, message: autogen_agentspeak.bdi.AgentSpeakMessage, ctx: MessageContext) -> None:
        self.on_receive(message, ctx)

