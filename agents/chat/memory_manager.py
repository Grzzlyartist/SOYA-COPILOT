from collections import deque


class MemoryManager:
    """Manages conversation memory for the chat agent."""
    
    def __init__(self, max_memory=4):
        """
        Initialize memory manager.
        
        Args:
            max_memory: Maximum number of message pairs to remember
        """
        self.conversation_memory = deque(maxlen=max_memory * 2)  # *2 for user+AI pairs

    def add_interaction(self, user_message, ai_response):
        """Add a user-AI interaction to memory."""
        self.conversation_memory.append({"role": "user", "content": user_message})
        self.conversation_memory.append({"role": "assistant", "content": ai_response})

    def get_recent_memory(self):
        """Get recent conversation history as a formatted string."""
        if not self.conversation_memory:
            return ""
        
        memory_str = ""
        for msg in self.conversation_memory:
            role = "User" if msg["role"] == "user" else "Assistant"
            memory_str += f"{role}: {msg['content']}\n"
        return memory_str

    def clear_memory(self):
        """Clear all conversation memory."""
        self.conversation_memory.clear()
