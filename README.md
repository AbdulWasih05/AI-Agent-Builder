# Ai Agent Builder

### Personal AI Academics Assignment

### Uploading on git just for version control

A small demo project to build, run and experiment with agentic AI. Designed for personal academic assignment and version control.

## Advanced Chatbot

A command-line chatbot with **persistent conversation history** is included in `chatbot.py`.

### Current Features

**Feature 1: Conversation History** ✅
- Stores the last 10 messages in memory during the session.
- Type `history` to view the full conversation.

**Feature 2: Persistent File Storage** ✅
- Saves all messages to `chat_history.json` automatically.
- Loads previous conversations when you start the chatbot.
- History persists across sessions!
- Type `clear` to start a fresh conversation (removes old history).

### Quick Start

Run it with Python (PowerShell on Windows):

```powershell
python chatbot.py
```




### How History is Persisted

- **In-memory buffer** — Last 10 messages stored in the `messages` list.
- **JSON file** — Each message is automatically saved to `chat_history.json`.
- **Auto-load** — On startup, the chatbot loads the previous conversation.
- **Rolling window** — Only the last 10 messages are kept (oldest removed first).


