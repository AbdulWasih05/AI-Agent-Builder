
"""
CLI chatbot with persistent conversation history.

Features:
- Stores conversation history (last 10 messages in memory)
- Saves history to a JSON file for persistence
- Loads previous conversations on startup
- Allows you to view the chat history
- Supports basic keyword-based responses

Type 'exit', 'quit' or press Ctrl+C to end the session.
Type 'history' to see the conversation so far.
Type 'clear' to start a fresh conversation.
"""

import sys
import json
import random
from typing import List, Tuple
from pathlib import Path

RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What would you like to talk about?",
    "help": "I can chat with you and remember our conversation. Type 'history' to see what we've talked about, or just keep chatting!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome!",
    "thank you": "Happy to help!",
}

FALLBACKS = [
    "I'm not sure I understand. Can you rephrase?",
    "Interesting — tell me more.",
    "Hmm, I don't have a good answer for that yet.",
]

EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye"}


class ConversationHistory:
    """Store and retrieve conversation messages with file persistence."""
    
    def __init__(self, max_size: int = 10, history_file: str = "chat_history.json"):
        self.messages: List[Tuple[str, str]] = []  # (speaker, text)
        self.max_size = max_size
        self.history_file = Path(history_file)
        self.load_from_file()
    
    def load_from_file(self) -> None:
        """Load conversation history from JSON file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Keep only the last max_size messages
                    self.messages = [tuple(msg) for msg in data[-self.max_size:]]
            except (json.JSONDecodeError, IOError):
                self.messages = []
    
    def save_to_file(self) -> None:
        """Save conversation history to JSON file."""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")
    
    def add(self, speaker: str, text: str) -> None:
        """Add a message to history and save."""
        self.messages.append((speaker, text))
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
        self.save_to_file()
    
    def display(self) -> str:
        """Return formatted history for display."""
        if not self.messages:
            return "No conversation history yet."
        
        lines = ["📝 Conversation History:"]
        for speaker, text in self.messages:
            prefix = "You" if speaker == "user" else "Bot"
            lines.append(f"  {prefix}: {text}")
        return "\n".join(lines)
    
    def clear(self) -> None:
        """Clear all history."""
        self.messages = []
        self.save_to_file()


def get_response(message: str) -> str:
    """Return a response based on keyword matching."""
    if not message.strip():
        return "Say something so I can respond!"

    msg = message.lower()
    
    # Check for keyword matches
    for keyword, response in RESPONSES.items():
        if keyword in msg:
            return response
    
    # Fallback response
    return random.choice(FALLBACKS)


def main() -> None:
    print("Chatbot with Persistent History — type 'history' to see your chat, 'clear' to reset, or 'exit' to leave\n")
    
    history = ConversationHistory()
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("Bot: Say something — I'm listening.\n")
                continue
            
            # Check for exit
            if user_input.lower() in EXIT_KEYWORDS:
                print("Bot: Goodbye! (History saved to chat_history.json)\n")
                break
            
            # Check for history command
            if user_input.lower() == "history":
                print(f"Bot: {history.display()}\n")
                history.add("user", user_input)
                continue
            
            # Check for clear command
            if user_input.lower() == "clear":
                history.clear()
                print("Bot: Conversation history cleared!\n")
                continue
            
            # Record user message
            history.add("user", user_input)
            
            # Generate and display response
            response = get_response(user_input)
            history.add("bot", response)
            print(f"Bot: {response}\n")
    
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye! (History saved to chat_history.json)\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
