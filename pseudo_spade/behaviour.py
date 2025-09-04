import asyncio
import collections
import logging
import time
import traceback
from abc import ABCMeta, abstractmethod
from asyncio import CancelledError
from datetime import timedelta, datetime
from threading import Event
from typing import Any, Optional, Dict, TypeVar

from .message import Message
from .template import Template

now = datetime.now

logger = logging.getLogger("spade.behaviour")

BehaviourType = TypeVar("BehaviourType", bound="CyclicBehaviour")


class BehaviourNotFinishedException(Exception):
    """ """

    pass


class NotValidState(Exception):
    """ """

    pass


class NotValidTransition(Exception):
    """ """

    pass


class CyclicBehaviour(object, metaclass=ABCMeta):
    """This behaviour is executed cyclically until it is stopped."""

    def __init__(self):
        self.agent = None
        self.template = None
        self._force_kill = Event()
        self._is_done = None
        self._exit_code = 0
        self.presence = None
        self.web = None
        self.is_running = False

        self.queue = None

    def set_agent(self, agent) -> None:
        """
        Links behaviour with its owner agent

        Args:
          agent (spade.agent.Agent): the agent who owns the behaviour

        """
        self.agent = agent
        asyncio.set_event_loop(self.agent.loop)
        self._is_done = asyncio.Event()
        self._is_done.set()
        self.queue = asyncio.Queue()
        self.presence = agent.presence
        self.web = agent.web

    def set_template(self, template: Template) -> None:
        """
        Sets the template that is used to match incoming
        messages with this behaviour.

        Args:
          template (spade.template.Template): the template to match with

        """
        self.template = template

    def match(self, message: Message) -> bool:
        """
        Matches a message with the behaviour's template

        Args:
          message(spade.message.Message): the message to match with

        Returns:
          bool: wheter the messaged matches or not

        """
        if self.template:
            return self.template.match(message)
        return True

    def set(self, name: str, value: Any) -> None:
        """
        Stores a knowledge item in the agent knowledge base.

        Args:
          name (str): name of the item
          value (Any): value of the item

        """
        self.agent.set(name, value)

    def get(self, name: str) -> Any:
        """
        Recovers a knowledge item from the agent's knowledge base.

        Args:
          name (str): name of the item

        Returns:
          Any: the object retrieved or None

        """
        return self.agent.get(name)

    def start(self) -> None:
        """starts behaviour in the event loop"""
        self.agent.submit(self._start())
        self.is_running = True

    async def _start(self) -> None:
        """
        Start coroutine. runs on_start coroutine and then
        runs the _step coroutine where the body of the behaviour
        is called.
        """
        await self.agent._alive.wait()
        try:
            await self.on_start()
        except Exception as e:
            logger.error(
                "Exception running on_start in behaviour {}: {}".format(self, e)
            )
            self.kill(exit_code=e)
        await self._step()
        self._is_done.clear()

    def kill(self, exit_code: Optional[Any] = None) -> None:
        """
        Stops the behaviour

        Args:
          exit_code (object, optional): the exit code of the behaviour (Default value = None)

        """
        self._force_kill.set()
        if exit_code is not None:
            self._exit_code = exit_code
        logger.info("Killing behavior {0} with exit code: {1}".format(self, exit_code))

    def is_killed(self) -> bool:
        """
        Checks if the behaviour was killed by means of the kill() method.

        Returns:
          bool: whether the behaviour is killed or not

        """
        return self._force_kill.is_set()

    @property
    def exit_code(self) -> Any:
        """
        Returns the exit_code of the behaviour.
        It only works when the behaviour is done or killed,
        otherwise it raises an exception.

        Returns:
          object: the exit code of the behaviour

        Raises:
            BehaviourNotFinishedException: if the behaviour is not yet finished

        """
        if self._done() or self.is_killed():
            return self._exit_code
        else:
            raise BehaviourNotFinishedException

    @exit_code.setter
    def exit_code(self, value: Any) -> None:
        """
        Sets a new exit code to the behaviour.

        Args:
          value (object): the new exit code

        """
        self._exit_code = value

    def _done(self) -> bool:
        """
        Returns True if the behaviour has finished
        else returns False

        Returns:
          bool: whether the behaviour is finished or not

        """
        return False

    def is_done(self) -> bool:
        """
        Check if the behaviour is finished

        Returns:
             bool: whether the behaviour is finished or not
        """
        return not self._is_done.is_set()

    async def join(self, timeout: Optional[float] = None) -> None:
        """
        Wait for the behaviour to complete

        Args:
            timeout (Optional[float]): an optional timeout to wait to join (if None, the join is blocking)

        Returns:
            None

        Raises:
            TimeoutError: if the timeout is reached
        """

        return await self._async_join(timeout=timeout)

    async def _async_join(self, timeout: Optional[float]) -> None:
        """
        Coroutine to wait until a behaviour is finished

        Args:
            timeout (Optional[float]): an optional timeout to wait to join

        Raises:
            TimeoutError: fi the timeout is reached
        """
        t_start = time.time()
        while not self.is_done():
            await asyncio.sleep(0.001)
            t = time.time()
            if timeout is not None and t - t_start > timeout:
                raise TimeoutError

    async def on_start(self) -> None:
        """
        Coroutine called before the behaviour is started.
        """
        pass

    async def on_end(self) -> None:
        """
        Coroutine called after the behaviour is done or killed.
        """
        pass

    @abstractmethod
    async def run(self) -> None:
        """
        Body of the behaviour.
        To be implemented by user.
        """
        raise NotImplementedError  # pragma: no cover

    async def _run(self) -> None:
        """
        Function to be overload by more complex behaviours.
        In other case it just calls run() coroutine.
        """
        await self.run()

    async def _step(self) -> None:
        """
        Main loop of the behaviour.
        checks whether behaviour is done or killed,
        ortherwise it calls run() coroutine.
        """
        cancelled = False
        while not self._done() and not self.is_killed():
            try:
                await self._run()
                await asyncio.sleep(0)  # relinquish cpu
            except CancelledError:  # pragma: no cover
                logger.debug("Behaviour {} cancelled".format(self))
                cancelled = True
            except Exception as e:
                logger.error(
                    "Exception running behaviour {behav}: {exc}".format(
                        behav=self, exc=e
                    )
                )
                logger.error(traceback.format_exc())
                self.kill(exit_code=e)
        try:
            if not cancelled:
                await self.on_end()
        except Exception as e:
            logger.error("Exception running on_end in behaviour {}: {}".format(self, e))
            self.kill(exit_code=e)
        self.is_running = False
        self.agent.remove_behaviour(self)

    async def enqueue(self, message: Message) -> None:
        """
        Enqueues a message in the behaviour's mailbox

        Args:
            message (spade.message.Message): the message to be enqueued
        """
        asyncio.create_task(self.queue.put(message))

    def mailbox_size(self) -> int:
        """
        Checks if there is a message in the mailbox

        Returns:
          int: the number of messages in the mailbox

        """
        return self.queue.qsize()

    async def send(self, msg: Message) -> None:
        """
        Sends a message.

        Args:
            msg (spade.message.Message): the message to be sent.
        """
        if msg.empty_sender():
            msg.sender = str(self.agent.jid)
            logger.debug(f"Adding agent's jid as sender to message: {msg}")
        await self.agent.container.send(msg, self)
        msg.sent = True
        self.agent.traces.append(msg, category=str(self))



    async def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        """
        Receives a message for this behaviour.
        If timeout is not None it returns the message or "None"
        after timeout is done.

        Args:
            timeout (float, optional): number of seconds until return

        Returns:
            spade.message.Message: a Message or None
        """
        if timeout:
            coro = self.queue.get()
            try:
                msg = await asyncio.wait_for(coro, timeout=timeout)
            except asyncio.TimeoutError:
                msg = None
        else:
            try:
                msg = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                msg = None
        return msg

    def __str__(self) -> str:
        return "{}/{}".format(
            "/".join(base.__name__ for base in self.__class__.__bases__),
            self.__class__.__name__,
        )


class OneShotBehaviour(CyclicBehaviour, metaclass=ABCMeta):
    """This behaviour is only executed once"""

    def __init__(self):
        super().__init__()
        self._already_executed = False

    def _done(self) -> bool:
        """ """
        if not self._already_executed:
            self._already_executed = True
            return False
        return True

