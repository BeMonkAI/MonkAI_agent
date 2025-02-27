import time
from .types  import Agent
from abc import ABC, abstractmethod

class Memory(ABC):
    """
    Abstract class for creating memory instances.

    This class provides a blueprint for creating different types of memory
    based on the system's needs. It includes methods to filter memory based
    on agent and time limits.

    """
    @abstractmethod
    def filter_memory(self, *args):
        """
        Filters memory based on the agent.

        """
        pass
    
    @abstractmethod
    def get_messages(self):
        pass

    @abstractmethod
    def get_last_message(self):
        """
        Returns the last message in memory.

        """
        pass

    @abstractmethod
    def get_memory_by_message_limit(self, limit):
        """
        Returns memory based on the message limit.

        """
        pass

    @abstractmethod
    def get_memory_by_time_limit(self, time_limit):
        """
        Returns memory based on the time limit.

        """
        pass
class AgentMemory(Memory):
    def __init__(self, initial_memory=[]):
        self.__messages = initial_memory      

    def get_messages(self):
        return self.__messages
    
    def filter_memory(self, *args):
        if len(args) == 1:
            return self.__filter_memory_by_agent(args[0])
        else:
            return self.__messages

    def __filter_memory_by_agent(self, agent:Agent):
        result = []
        for msg in self.__messages:
           if msg['agent'] == agent.name or  msg['agent'] is None or  (agent.predecessor_agent is not None and msg['agent'] == agent.predecessor_agent.name):
               result.append(msg)
        return result
    
    def get_last_message(self):
       return self.__messages[-1]     

    def append(self, message):
        self.__messages.append(message)

    def get_memory_by_message_limit(self, limit):
        return self.__messages[-limit:]

    def get_memory_by_time_limit(self, time_limit):
        current_time = time.time()
        return [msg for msg in self.__messages if current_time - msg['inserted_at'] <= time_limit]