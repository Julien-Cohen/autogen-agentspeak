import asyncio
import collections
import ast

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib
from autogen_core import RoutedAgent, TopicId, MessageContext

from dataclasses import dataclass


@dataclass
class CatalogEntry:
    achievement: str
    arity: int
    meaning: str


def lit_of_str(s: str) -> agentspeak.Literal:
    l = s.split(sep="(", maxsplit=1)
    symb = l[0]
    if len(l) == 1:
        return agentspeak.Literal(symb)
    else:
        rest = l[1]
        assert rest.endswith(")")
        args = rest.removesuffix(")")
        if args.startswith("_X_"):
            return agentspeak.Literal(symb, agentspeak.Var)
        else:
            t = ast.literal_eval(args)
            if isinstance(t, tuple):
                return agentspeak.Literal(symb, t)
            else:
                return agentspeak.Literal(symb, (t,))


def strplan(p: str):
    return agentspeak.Literal("plain_text", (p,))


def add_source(lit: agentspeak.Literal, s: str) -> agentspeak.Literal:
    return lit.with_annotation(agentspeak.Literal("source", (agentspeak.Literal(s),)))


@dataclass
class AgentSpeakMessage:
    illocution: str
    content: str
    sender: str

    def goal_type(self) -> agentspeak.GoalType:
        _i = self.illocution
        if _i == "tell" or _i == "untell":
            return agentspeak.GoalType.belief
        elif _i == "achieve" or _i == "unachieve":
            return agentspeak.GoalType.achievement
        elif _i == "tellHow" or _i == "untellHow":
            return agentspeak.GoalType.tellHow
        else:
            raise RuntimeError("Illocution not supported: " + _i)

    def trigger(self) -> agentspeak.Trigger:
        _i = self.illocution
        if _i == "tell" or _i == "achieve" or _i == "tellHow":
            return agentspeak.Trigger.addition
        elif _i == "untell" or _i == "unachieve" or _i == "untellHow":
            return agentspeak.Trigger.removal
        else:
            raise RuntimeError("Illocution not supported: " + _i)

    def literal(self) -> agentspeak.Literal:
        _i = self.illocution
        _c = self.content
        _s = self.sender
        if _i in ["tell", "untell", "achieve", "unachieve"]:
            return add_source(lit_of_str(_c).freeze({}, {}), _s)
        elif _i in ["tellHow", "untellHow"]:
            return add_source(strplan(_c).freeze({}, {}), _s)
        else:
            raise RuntimeError("Illocution not supported: " + _i)


class BDIAgent(RoutedAgent):

    def __init__(self, descr, asl_file):

        # FIXME : self.bdi_intention_buffer not used in this version
        self.bdi_intention_buffer = collections.deque()
        super().__init__(descr)
        self.published_commands = []

        self.env = agentspeak.runtime.Environment()

        # add custom actions (must occur before loading the asl file)
        self.bdi_actions = agentspeak.Actions(agentspeak.stdlib.actions)
        self.add_custom_actions(self.bdi_actions)

        with open(asl_file) as source:
            self.asp_agent = self.env.build_agent(source, self.bdi_actions)

        self.env.run()

    # this method is called by __init__
    def add_custom_actions(self, actions: agentspeak.Actions):

        # Action jump for testing
        @actions.add("jump", 0)
        def _jump(a: agentspeak.runtime.Agent, b, c):
            print("[" + a.name + "] I jump")
            yield

        @actions.add_procedure(
            ".send",
            (
                agentspeak.Literal,
                agentspeak.Literal,
                agentspeak.Literal,
            ),
        )
        def _autogen_send(topic, illoc, lit):
            # (self.publish_message is defined with the async keyword)
            asyncio.create_task(
                self.publish_message(
                    AgentSpeakMessage(
                        illocution=str(illoc),
                        content=str(lit),
                        sender=str(self.asp_agent.name),
                    ),
                    topic_id=TopicId(str(topic), source="default"),
                )
            )

        @actions.add_procedure(
            ".send_plan",
            (
                agentspeak.Literal,
                agentspeak.Literal,
                str,
            ),
        )
        def _autogen_send_plan(topic, illoc, lit):
            asyncio.create_task(
                self.publish_message(
                    AgentSpeakMessage(
                        illocution=str(illoc),
                        content=lit,
                        sender=str(self.asp_agent.name),
                    ),
                    topic_id=TopicId(str(topic), source="default"),
                )
            )

        @actions.add_procedure(
            ".set_public",
            (agentspeak.Literal, int, str),
        )
        def _set_public(command: agentspeak.Literal, arity: int, doc: str):
            self.register_command(command.functor, arity, doc)

        @actions.add_procedure(
            ".send_catalog",
            (agentspeak.Literal,),
        )
        def _send_catalog(topic):
            asyncio.create_task(
                self.publish_message(
                    AgentSpeakMessage(
                        illocution="tell",
                        content="catalog(" + str(self.published_commands) + ")",
                        sender=str(self.asp_agent.name),
                    ),
                    topic_id=TopicId(str(topic), source="default"),
                )
            )

    def on_receive(self, msg: AgentSpeakMessage, ctx: MessageContext):
        self.asp_agent.call(
            msg.trigger(),
            msg.goal_type(),
            msg.literal(),
            agentspeak.runtime.Intention(),
        )
        self.env.run()

    def register_command(self, command, arity, doc):
        """This procedure inserts an achievement with its documentation in the catalog of this agent,
        which will be able to publish it to tell others how to use it."""
        self.published_commands.append(CatalogEntry(command, arity, doc))
