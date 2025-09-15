import asyncio
import collections
import re
import ast

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, TopicId, MessageContext

from dataclasses import dataclass

@dataclass
class AgentSpeakMessage:
    illocution: str
    content: str
    sender: str

# from https://github.com/sfp932705/spade_bdi/blob/master/spade_bdi/bdi.py
# Warning: github repository for spade-bdi is stuck at v0.1.4 while on Pypi 0.3.2
def parse_literal(msg):
    functor = msg.split("(")[0]

    if "(" in msg:
        args = msg.split("(")[1]
        args = args.split(")")[0]

        x = re.search("^_X_*", args)

        if x is not None:
            args = agentspeak.Var()
        else:
            args = ast.literal_eval(args)

        def recursion(arg):
            if isinstance(arg, list):
                return tuple(recursion(i) for i in arg)
            return arg

        new_args = (recursion(args),)

    else:
        new_args = ""
    return functor, new_args



class BDIAgent(RoutedAgent):

    def __init__(self, descr, asl_file):
        self.bdi_intention_buffer = collections.deque()
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

            @actions.add_function(".name",())
            def _name():
                return self.asp_agent.name

            @actions.add("jump",0)
            def _jump(a: agentspeak.runtime.Agent, b, c):
                print("["+ a.name +"] I jump")
                yield

            @actions.add_procedure(
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
                    topic_id=TopicId(str(topic), source="default")
                ))


    def on_receive(self, msg: AgentSpeakMessage, ctx: MessageContext):

        # from spade-bdi 0.3.2, file bdi.py
        ilf_type = msg.illocution
        if ilf_type == "tell":
            goal_type = agentspeak.GoalType.belief
            trigger = agentspeak.Trigger.addition
        elif ilf_type == "untell":
            goal_type = agentspeak.GoalType.belief
            trigger = agentspeak.Trigger.removal
        elif ilf_type == "achieve":
            goal_type = agentspeak.GoalType.achievement
            trigger = agentspeak.Trigger.addition
        elif ilf_type == "unachieve":
            goal_type = agentspeak.GoalType.achievement
            trigger = agentspeak.Trigger.removal
        elif ilf_type == "tellHow":
            goal_type = agentspeak.GoalType.tellHow
            trigger = agentspeak.Trigger.addition
        elif ilf_type == "untellHow":
            goal_type = agentspeak.GoalType.tellHow
            trigger = agentspeak.Trigger.removal
        elif ilf_type == "askHow":
            goal_type = agentspeak.GoalType.askHow
            trigger = agentspeak.Trigger.addition
        else:
            raise agentspeak.AslError("unknown illocutionary force: {}".format(ilf_type))

        intention = agentspeak.runtime.Intention()

        ###
        if ilf_type in ["tellHow", "untellHow"]:
            message = agentspeak.Literal("plain_text", (msg.content,), frozenset())
        elif ilf_type == "askHow":
            raise Exception("Not supported yet") # fixme
        #    message = agentspeak.Literal("plain_text", (msg.content,), frozenset())

        #    def _call_ask_how(self, receiver, message, intention):
                # message.args[0] is the string plan to be sent
        #        body = agentspeak.asl_str(
        #            agentspeak.freeze(message.args[0], intention.scope, {})
        #        )
        #        mdata = {
        #            "performative": "BDI",
        #            "ilf_type": "tellHow",
        #        }
        #        msg = Message(to=receiver, body=body, metadata=mdata)
        #        _call_ask_how.spade_agent.submit(
        #            _call_ask_how.spade_class.send(msg)
        #        )

        #    _call_ask_how.spade_agent = self.agent

        #    _call_ask_how.spade_class = self

        #    agentspeak.runtime.Agent._call_ask_how = _call_ask_how

            # Overrides function ask_how from module agentspeak
        #    agentspeak.runtime.Agent._ask_how = _ask_how

        else:
            # Sends a literal
            functor, args = parse_literal(msg.content)

            message = agentspeak.Literal(functor, args)

        message = agentspeak.freeze(message, intention.scope, {})

        # Add source to message
        tagged_message = message.with_annotation(
            agentspeak.Literal("source", (agentspeak.Literal(str(msg.sender)),))
        )
        if ilf_type == "tellHow":
            pass

        self.bdi_intention_buffer.append(
            (trigger, goal_type, tagged_message, intention)
        )

        if self.bdi_intention_buffer:
            temp_intentions = collections.deque(self.bdi_intention_buffer)
            for trigger, goal_type, term, intention in temp_intentions:
                self.asp_agent.call(trigger, goal_type, term, intention)
                self.bdi_intention_buffer.popleft()

        self.env.run()

