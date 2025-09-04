import logging
from typing import Optional, Dict, Union, Type

import autogen_core

#from slixmpp import ClientXMPP
#from slixmpp.plugins.xep_0004.stanza.form import Form
#from slixmpp import JID
#from slixmpp.stanza import Message as SlixmppMessage

SPADE_X_METADATA = "spade:x:metadata"

logger = logging.getLogger("spade.Message")


class MessageBase(object):
    """Base class for message handling in SPADE."""

    def __init__(
        self,
        to: Union[str, autogen_core.AgentId, None] = None,
        sender: Union[str, autogen_core.AgentId, None] = None,
        body: Optional[str] = None,
        thread: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.sent = False
        self.to = to  # type: ignore
        self.sender = sender  # type: ignore
        self.body = body
        self.thread = thread

        if metadata is None:
            self.metadata = {}
        else:
            for key, value in metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise TypeError("Key and Value of metadata MUST be strings")
            self.metadata = metadata


    @property
    def to(self) -> autogen_core.AgentId:
        """
        Gets the id of the receiver.

        Returns:
          autogen_core.AgentId: id of the receiver

        """
        return self._to

    @to.setter
    def to(self, id: Union[str, autogen_core.AgentId, None]) -> None:
        """
        Set id of the receiver.

        Args:
          id (str): the id of the receiver.

        """
        if id is None:
            self._to = None # fixme
        elif isinstance(id, str):
            self._to = None # fixme
        elif isinstance(id, autogen_core.AgentId):
            self._to = id
        else:
            raise TypeError("'to' MUST be a valid ID, str or None")

    @property
    def sender(self) -> autogen_core.AgentId:
        """
        Get jid of the sender

        Returns:
          slixmpp.JID: jid of the sender

        """
        return self._sender

    @sender.setter
    def sender(self, id: Union[str, autogen_core.AgentId, None]) -> None:
        """
        Set id of the sender

        Args:
          id (str): jid of the sender

        """
        if id is None:
            self._sender = None #fixme
        elif isinstance(id, str):
            self._sender = None #fixme
        elif isinstance(id, autogen_core.AgentId):
            self._sender = id
        else:
            raise TypeError("'sender' MUST be a valid JID, str or None")

    @property
    def body(self) -> Union[str, None]:
        """
        Get body of the message
        Returns:
            str: the body of the message
        """
        return self._body

    @body.setter
    def body(self, body: Union[str, None]) -> None:
        """
        Set body of the message
        Args:
            body (str): The body of the message
        """
        if body is None:
            self._body = ""
        elif not isinstance(body, str):
            raise TypeError("'body' MUST be a string")
        self._body = body  # type: ignore

    @property
    def thread(self) -> Union[str, None]:
        """
        Get Thread of the message

        Returns:
            str: thread id
        """
        return self._thread

    @thread.setter
    def thread(self, value: Union[str, None]) -> None:
        """
        Set thread id of the message

        Args:
            value (str): the thread id

        """
        if value is not None and not isinstance(value, str):
            raise TypeError("'thread' MUST be a string")
        self._thread = value

    def set_metadata(self, key: str, value: str) -> None:
        """
        Add a new metadata to the message

        Args:
          key (str): name of the metadata
          value (str): value of the metadata

        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("'key' and 'value' of metadata MUST be strings")
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Union[str, None]:
        """
        Get the value of a metadata. Returns None if metadata does not exist.

        Args:
          key (str): name of the metadata

        Returns:
          str: the value of the metadata (or None)

        """
        return self.metadata[key] if key in self.metadata else None

    @staticmethod
    def empty_jid(id: autogen_core.AgentId):
        return not id.bare and not id.domain and not id.resource

    def empty_to(self):
        return self.empty_jid(self.to)

    def empty_sender(self):
        return self.empty_jid(self.sender)

    def match(self, message: "MessageBase") -> bool:
        """
        Returns wether a message matches with this message or not.
        The message can be a Message object or a Template object.

        Args:
          message (spade.message.Message): the message to match to

        Returns:
          bool: wether the message matches or not

        """
        if not self.empty_to() and not message.to.__eq__(self.to):
            return False

        if not self.empty_sender() and not message.sender.__eq__(self.sender):
            return False

        if self.body and message.body != self.body:
            return False

        if self.thread and (message.thread is None or message.thread != self.thread):
            return False

        for key, value in self.metadata.items():
            if message.get_metadata(key) != value:
                return False

        logger.debug(f"message matched {self} == {message}")
        return True

    @property
    def id(self) -> int:
        """ """
        return id(self)

    def __eq__(self, other: object):
        if not isinstance(other, Message):
            return False
        return self.match(other) and other.match(self)


class Message(MessageBase):
    """ """

    def make_reply(self) -> "Message":
        """
        Creates a copy of the message, exchanging sender and receiver

        Returns:
          spade.message.Message: a new message with exchanged sender and receiver

        """
        return Message(
            to=str(self.sender),
            sender=str(self.to),
            body=self.body,
            thread=self.thread,
            metadata=self.metadata,
        )

    def __str__(self) -> str:
        s = f'<message to="{self.to}" from="{self.sender}" thread="{self.thread}" metadata={self.metadata}>'
        if self.body:
            s += "\n" + self.body + "\n"
        s += "</message>"
        return s
