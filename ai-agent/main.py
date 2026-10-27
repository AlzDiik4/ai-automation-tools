import json
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AIAgentPipeline:
    """
    Automated AI Task Processing Pipeline.
    Handles input validation, context building, and structured payload execution.
    """
    def __init__(self, agent_name: str, config: Dict[str, Any]):
        self.agent_name = agent_name
        self.config = config
        self.memory_buffer: List[Dict[str, str]] = []

    def load_context(self, user_prompt: str) -> None:
        """Injects user prompt and maintains short-term conversational context."""
        self.memory_buffer.append({"role": "user", "content": user_prompt})
        logging.info(f"[{self.agent_name}] Context updated. Current buffer size: {len(self.memory_buffer)}")

    def build_payload(self) -> Dict[str, Any]:
        """Constructs API payload for model inference."""
        payload = {
            "agent": self.agent_name,
            "temperature": self.config.get("temperature", 0.7),
            "messages": self.memory_buffer,
            "stream": False
        }
        return payload

    def execute_step(self, user_prompt: str) -> Dict[str, Any]:
        """Runs single-step automated pipeline execution."""
        self.load_context(user_prompt)
        payload = self.build_payload()
        
        # Simulated agent response execution
        response = {
            "status": "success",
            "executed_by": self.agent_name,
            "output": f"Processed prompt: '{user_prompt}' via automated workflow."
        }
        
        self.memory_buffer.append({"role": "assistant", "content": response["output"]})
        logging.info(f"[{self.agent_name}] Step executed successfully.")
        return response

if __name__ == "__main__":
    agent_config = {"temperature": 0.2, "max_tokens": 1024}
    pipeline = AIAgentPipeline(agent_name="DataExtractorAgent", config=agent_config)
    
    res = pipeline.execute_step("Extract structure from incoming log stream.")
    print(json.dumps(res, indent=2, ensure_ascii=False))