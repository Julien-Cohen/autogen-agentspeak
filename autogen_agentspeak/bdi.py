import asyncio
import os
from ast import literal_eval

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, TopicId

from dataclasses import dataclass

@dataclass
class AgentSpeakMessage:
    illocution: str
    content: str
    sender: str

# from https://github.com/sfp932705/spade_bdi/blob/master/spade_bdi/bdi.py
def parse_literal(msg):
    functor = msg.split("(")[0]
    if "(" in msg:
        args = msg.split("(")[1]
        args = args.split(")")[0]
        args = literal_eval(args)

        def recursion(arg):
            if isinstance(arg, list):
                return tuple(recursion(i) for i in arg)
            return arg

        new_args = (recursion(args),)

    else:
        new_args = ''
    return functor, new_args



class BDIAgent(RoutedAgent):

    def __init__(self, descr, asl_file):
        super().__init__(descr)

        self.env = agentspeak.runtime.Environment()

        # add custom actions (must occur before loading the asl file)
        self.bdi_actions = agentspeak.Actions(agentspeak.stdlib.actions)
        self.add_custom_actions(self.bdi_actions)

        with open(asl_file) as source:
            self.asp_agent=self.env.build_agent(source, self.bdi_actions)

        self.env.run()

    # this method is called by __init__
    def add_custom_actions(self, actions):
            # custom action
            @actions.add_function(
                ".autogen_send",
                (
                        agentspeak.Literal,
                        agentspeak.Literal,
                        agentspeak.Literal,
                ),
            )
            def _autogen_send(topic, illoc, lit):
                # (self.publish_message is defined with the async keyword)
                asyncio.create_task(self.publish_message(
                    AgentSpeakMessage(
                        illocution = str(illoc),
                        content    = str(lit),
                        sender     = str(self.asp_agent.name)
                    ),
                    topic_id=TopicId(str(topic), source="default"),
                ))

    # Inspired from https://github.com/sfp932705/spade_bdi/blob/master/spade_bdi/bdi.py
    def on_receive(self, message: AgentSpeakMessage):
        if message.illocution == "tell":
            goal_type = agentspeak.GoalType.belief
            trigger = agentspeak.Trigger.addition
        elif message.illocution == "achieve":
            goal_type = agentspeak.GoalType.achievement
            trigger = agentspeak.Trigger.addition
        else:
            raise agentspeak.AslError("unknown illocutionary force: {}".format(message.illocution))

        intention = agentspeak.runtime.Intention()
        (functor, args) = parse_literal(message.content)

        m = agentspeak.Literal(functor, args)

        tagged_m = m.with_annotation(agentspeak.Literal("source", (agentspeak.Literal(str(message.sender)),)))

        self.asp_agent.call(
            trigger,
            goal_type,
            tagged_m,
            intention)

        self.env.run()

