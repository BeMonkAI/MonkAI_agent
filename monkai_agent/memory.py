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
    def __init__(self, initial_memory=[], limit=-1):
        self.__messages = initial_memory   
        self.__limit = limit   

    def delete_invalid_messages(self, messages):
        valid_messages = []
        for i, msg in enumerate(messages):
            if msg['role'] == 'tool':
                if i == 0:
                    continue
                if messages[i-1].get('tool_calls') is None :
                    valid_messages.remove(valid_messages[-1])
                    continue
            valid_messages.append(msg)
        return valid_messages

    def get_messages(self):
        if self.__limit > 0:
            return self.delete_invalid_messages(self.__messages[-self.__limit:])
        return self.delete_invalid_messages(self.__messages)
    
    def filter_memory(self, *args):
        if len(args) == 1:
            return self.delete_invalid_messages(self.__filter_memory_by_agent(args[0]))
        else:
            return self.delete_invalid_messages(self.__messages)

    def __filter_memory_by_agent(self, agent:Agent):
        result = []
        for msg in self.__messages:
            if not 'agent' in msg:
                msg['agent'] = None
            if msg['agent'] == agent.name or  msg['agent'] is None or  (agent.predecessor_agent is not None and msg['agent'] == agent.predecessor_agent.name):
               result.append(msg)
            elif agent.sucessors_agent:
                for sucessor in agent.sucessors_agent:
                    if msg['agent'] == sucessor.name:
                        result.append(msg)
                        break
        if self.__limit > 0:
            return result[-self.__limit:]
        return result
    
    def get_last_message(self):
       return self.__messages[-1]     

    def append(self, message):
        self.__messages.append(message)

    def extend(self, messages):
        self.__messages.extend(messages)

    def get_memory_by_message_limit(self, limit):
        return self.delete_invalid_messages(self.__messages[-limit:])

    def get_memory_by_time_limit(self, time_limit):
        current_time = time.time()
        return self.delete_invalid_messages([msg for msg in self.__messages if current_time - msg['inserted_at'] <= time_limit])
    
    
            
