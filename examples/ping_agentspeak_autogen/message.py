from dataclasses import dataclass

asp_message = "ASP_MESSAGE"

@dataclass
class MyMessage:
    illocution: str
    content: str
