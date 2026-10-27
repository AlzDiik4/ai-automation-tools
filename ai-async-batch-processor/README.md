# AI Async Batch Processor

Asynchronous concurrency orchestrator for high-throughput LLM tasks and batch processing pipelines.

## Features
- **Concurrency Limiting:** `asyncio.Semaphore` prevents rate-limit explosions on external APIs.
- **Fault Tolerance:** `return_exceptions=True` ensures partial batch failures don't crash the entire pipeline.
- **Detailed Telemetry:** Clean structured logging for execution tracking.

## Quickstart
```bash
python async_processor.py