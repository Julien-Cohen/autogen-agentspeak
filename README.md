# autogen-agentspeak

Implement BDI Agents based on the AutoGen MAS Platform.

Inspired by [spade-bdi](https://github.com/sfp932705/spade_bdi) that powers design of Spade agents based on AgentSpeak source code,
autogen-agentspeak (this module) enables the design of AutoGen agents based on AgentSpeak code.

# Requirements
This module relies on AutoGen (package autogen-core) and [python-agentspeak](https://github.com/niklasf/python-agentspeak) (package agentspeak). 
See `requirements.txt` for matching version.

### Optional
 To run the examples that use an LLM, you must install the package `autogen-ext[openai]`
and set your OPENAI_API_KEY in the environment.
 To use another LLM just fix the following lines in each example source code.

```
model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
    )
```


# Current state
This is work in progress. See the examples and tests to lear how to use.

# Credits
The source code of this module is partly based on the source code of [spade-bdi](https://github.com/sfp932705/spade_bdi) (see `bdi.py`).

