# Short-term memory module to keep trackof recent conversation history, like around 10 turns to not overuse tokens

class ShortTermMemory:
    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns

    def add(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })
        # keeping only the last 'max_turns' turns (user+hawking = 2 messages per turn)
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def format_for_prompt(self):
        formatted = ""
        for msg in self.history:
            if msg["role"] == "user":
                formatted += f"User: {msg['content']}\n"
            else:
                formatted += f"Hawking: {msg['content']}\n"
        return formatted.strip()