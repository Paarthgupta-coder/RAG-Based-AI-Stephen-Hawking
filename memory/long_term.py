import json
import os
from datetime import datetime

MEMORY_FILE = "memory/long_term_memory.json"

class LongTermMemory:
    def __init__(self):
        self.memories = []
        self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                self.memories = json.load(f)
        else:
            self.memories = []

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memories, f, indent=2)

    def add(self, fact):
        entry = {
            "fact": fact,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.memories.append(entry)
        self.save()

    def get_all(self):
        return self.memories

    def format_for_prompt(self):
        if not self.memories:
            return ""
        formatted = "Things I remember about this user from previous conversations:\n"
        for m in self.memories[-10:]:
            formatted += f"- {m['fact']}\n"
        return formatted.strip()

    def clear(self):
        self.memories = []
        self.save()