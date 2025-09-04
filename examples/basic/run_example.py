#inspired by https://github.com/javipalanca/spade_bdi/blob/master/examples/basic/run_example.py
import argparse
import asyncio
import getpass

import autogen_core

from autogen_agentspeak.bdi import BDIAgent


async def main(server, password):
    a = BDIAgent(f"bdiagent@{server}", password, "basic.asl")
    await a.start()

    await asyncio.sleep(1)

    a.bdi.set_belief("car", "azul", "big")
    a.bdi.print_beliefs()
    print("GETTING FIRST CAR BELIEF")
    print(a.bdi.get_belief("car"))
    a.bdi.print_beliefs()
    a.bdi.remove_belief("car", 'azul', "big")
    a.bdi.print_beliefs()
    print(a.bdi.get_beliefs())
    a.bdi.set_belief("car", 'amarillo')

    await a.stop()


