import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SlidingWindowContextManager:
    """
    Manages conversational context windows for LLM agents, 
    preventing token overflow by dropping oldest messages while preserving system prompts.
    """
    def __init__(self, max_token_limit: int = 4000):
        self.max_token_limit = max_token_limit
        self.system_prompt: Dict[str, str] = {"role": "system", "content": "You are an autonomous AI engineering assistant."}
        self.history: List[Dict[str, str]] = []

    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation: ~4 characters per token in English/code."""
        return max(1, len(text) // 4)

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt["content"] = prompt
        logging.info("System prompt updated.")

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        self._enforce_token_limit()

    def _enforce_token_limit(self) -> None:
        """Prunes oldest history messages if total estimated tokens exceed the limit."""
        while True:
            total_tokens = self._estimate_tokens(self.system_prompt["content"])
            for msg in self.history:
                total_tokens += self._estimate_tokens(msg["content"])

            if total_tokens <= self.max_token_limit or not self.history:
                break
            
            # Drop the oldest message from history
            removed = self.history.pop(0)
            logging.warning(f"Token limit exceeded ({total_tokens}/{self.max_token_limit}). Dropped oldest message from role: {removed['role']}")

    def get_full_payload(self) -> List[Dict[str, str]]:
        """Returns structured message payload ready for LLM API call."""
        return [self.system_prompt] + self.history

if __name__ == "__main__":
    manager = SlidingWindowContextManager(max_token_limit=100) # Small limit for demo
    
    manager.add_message("user", "Hello, can you help me optimize a memory allocator in C?")
    manager.add_message("assistant", "Yes, sure! Use arena allocation to avoid heap fragmentation.")
    manager.add_message("user", "Great, show me a quick implementation example.")
    
    payload = manager.get_full_payload()
    print(f"Final Payload Message Count: {len(payload)}")
    for msg in payload:
        print(f"[{msg['role'].upper()}]: {msg['content']}")