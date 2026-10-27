import asyncio
import logging
import random
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AsyncAIBatchProcessor:
    """
    Handles asynchronous batch execution of tasks with concurrency limiting (semaphores) 
    and robust error handling / retries.
    """
    def __init__(self, max_concurrency: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def simulate_model_inference(self, task_id: int, payload: str) -> Dict[str, Any]:
        async with self.semaphore:
            logging.info(f"Task {task_id}: Starting inference for payload: '{payload}'")
            # Simulate network latency of LLM API call
            delay = random.uniform(0.5, 1.5)
            await asyncio.sleep(delay)
            
            # Simulate random success/failure
            if random.random() < 0.1:
                raise RuntimeError(f"Task {task_id}: API rate limit or timeout error.")

            return {
                "task_id": task_id,
                "status": "success",
                "result": f"Processed '{payload}' in {delay:.2f}s"
            }

    async def run_batch(self, tasks: List[str]) -> List[Dict[str, Any]]:
        coros = [
            self.simulate_model_inference(i, task) 
            for i, task in enumerate(tasks, start=1)
        ]
        results = await asyncio.gather(*coros, return_exceptions=True)
        
        processed_output = []
        for idx, res in enumerate(results, start=1):
            if isinstance(res, Exception):
                logging.error(f"Task {idx} failed with exception: {res}")
                processed_output.append({"task_id": idx, "status": "failed", "error": str(res)})
            else:
                processed_output.append(res)
                
        return processed_output

if __name__ == "__main__":
    tasks_input = [
        "Analyze log error 502",
        "Generate unit tests for memory allocator",
        "Summarize documentation on Python asyncio",
        "Extract entities from support ticket #44",
        "Optimize SQL query execution plan"
    ]

    processor = AsyncAIBatchProcessor(max_concurrency=2)
    loop = asyncio.get_event_loop()
    final_results = loop.run_until_complete(processor.run_batch(tasks_input))

    print("\n--- Batch Execution Report ---")
    for r in final_results:
        print(r)