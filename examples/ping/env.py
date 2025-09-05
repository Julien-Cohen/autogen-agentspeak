#!/usr/bin/env python

import os

import agentspeak.runtime
import agentspeak.stdlib

env = agentspeak.runtime.Environment()

with open(os.path.join(os.path.dirname(__file__), "receiver.asl")) as source:
    env.build_agent(source, agentspeak.stdlib.actions)

with open(os.path.join(os.path.dirname(__file__), "sender.asl")) as source:
    env.build_agent(source, agentspeak.stdlib.actions)

if __name__ == "__main__":
    env.run()
