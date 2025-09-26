import dataclasses

asp_message_to_translator = "to_translator"
asp_message_to_asp_agent = "robot_agent"

@dataclasses.dataclass
class HumanMessage:
    human_content: str

@dataclasses.dataclass
class Command:
    content: str
