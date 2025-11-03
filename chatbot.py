
"""
CLI chatbot with conversation history tracking.

This is an enhanced version of the simple chatbot that now:
- Stores conversation history (last 10 messages)
- Allows you to view the chat history
- Supports basic keyword-based responses

Type 'exit', 'quit' or press Ctrl+C to end the session.
Type 'history' to see the conversation so far.
"""

import sys
import random
from typing import List, Tuple

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
    """Store and retrieve conversation messages."""
    
    def __init__(self, max_size: int = 10):
        self.messages: List[Tuple[str, str]] = []  # (speaker, text)
        self.max_size = max_size
    
    def add(self, speaker: str, text: str) -> None:
        """Add a message to history."""
        self.messages.append((speaker, text))
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
    
    def display(self) -> str:
        """Return formatted history for display."""
        if not self.messages:
            return "No conversation history yet."
        
        lines = ["📝 Conversation History:"]
        for speaker, text in self.messages:
            prefix = "You" if speaker == "user" else "Bot"
            lines.append(f"  {prefix}: {text}")
        return "\n".join(lines)


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
    print("Chatbot with History Tracking — type 'history' to see your chat, or 'exit' to leave\n")
    
    history = ConversationHistory()
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                print("Bot: Say something — I'm listening.\n")
                continue
            
            # Check for exit
            if user_input.lower() in EXIT_KEYWORDS:
                print("Bot: Goodbye!\n")
                break
            
            # Check for history command
            if user_input.lower() == "history":
                print(f"Bot: {history.display()}\n")
                history.add("user", user_input)
                continue
            
            # Record user message
            history.add("user", user_input)
            
            # Generate and display response
            response = get_response(user_input)
            history.add("bot", response)
            print(f"Bot: {response}\n")
    
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
