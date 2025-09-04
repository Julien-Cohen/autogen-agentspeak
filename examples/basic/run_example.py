#inspired by https://github.com/javipalanca/spade_bdi/blob/master/examples/basic/run_example.py
import argparse
import asyncio
import getpass

import autogen_core
from autogen_core import SingleThreadedAgentRuntime, AgentId

from autogen_agentspeak.bdi import BDIAgent

import autogen_agentchat.messages as messages

async def main():
    runtime = SingleThreadedAgentRuntime()



    await BDIAgent.register(
        runtime, type="truc", factory=lambda: BDIAgent("test", "basic.asl")
    )

    runtime.start()


    # Remark : the agent has not been instantiated yet
    await runtime.send_message(messages.TextMessage(content="Hello, World!", source="User"), AgentId("truc", "default"))


    """" a.bdi.set_belief("car", "azul", "big")
    a.bdi.print_beliefs()
    print("GETTING FIRST CAR BELIEF")
    print(a.bdi.get_belief("car"))
    a.bdi.print_beliefs()
    a.bdi.remove_belief("car", 'azul', "big")
    a.bdi.print_beliefs()
    print(a.bdi.get_beliefs())
    a.bdi.set_belief("car", 'amarillo')
 """
    await runtime.stop_when_idle()


asyncio.run(main())
