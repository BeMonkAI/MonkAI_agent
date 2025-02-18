import time
from .monkai_agent_creator  import MonkaiAgentCreator

class Memory:
    def __init__(self, agent:MonkaiAgentCreator, messages=[]):
        self.agent = agent
        self.messages = []
        for msg in messages:
           if msg['agent'] == agent.agent_name or msg['agent'] == agent.predecessor_agent.agent_name:
               self.messages.append(msg)

    def get_memory_by_message_limit(self, limit):
        return self.messages[-limit:]

    def get_memory_by_time_limit(self, time_limit):
        current_time = time.time()
        return [msg for msg in self.messages if current_time - msg['inserted_at'] <= time_limit]