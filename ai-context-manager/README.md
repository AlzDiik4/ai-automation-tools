# AI Context Window Manager

Lightweight sliding-window memory manager for LLM agents designed to prevent token limit overflow.

## Features
- **System Prompt Preservation:** Keeps core instructions locked while trimming history.
- **Dynamic Token Budgeting:** Automatically estimates payload size and prunes stale turns.
- **Clean API Integration:** Formats output directly for LLM chat completion endpoints.

## Quickstart
```bash
python context_manager.py