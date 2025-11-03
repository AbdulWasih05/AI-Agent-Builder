
"""
Simple CLI chatbot.

This is a tiny rule-based chatbot that looks for keywords and replies with canned answers.
Type 'exit', 'quit' or press Ctrl+C to end the session.
"""

import sys

RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What would you like to talk about?",
    "help": "I can chat about simple topics. Try saying 'hello', ask for 'help', or say 'bye' to exit.",
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


def get_response(message: str) -> str:
    """Return a canned response based on simple keyword matching."""
    if not message:
        return "Say something so I can respond!"

    msg = message.lower()
    for k, v in RESPONSES.items():
        if k in msg:
            return v

    if any(word in msg for word in EXIT_KEYWORDS):
        return "bye"

    # fallback
    import random

    return random.choice(FALLBACKS)


def main() -> None:
    print("Simple Chatbot — type 'exit' or 'quit' to leave")

    try:
        while True:
            user = input("You: ").strip()
            if not user:
                print("Bot: Say something — I'm listening.")
                continue

            if user.lower() in EXIT_KEYWORDS:
                print("Bot: Goodbye!")
                break

            resp = get_response(user)
            if resp == "bye":
                print("Bot: Goodbye!")
                break

            print(f"Bot: {resp}")
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye!")
        try:
            sys.exit(0)
        except SystemExit:
            pass


if __name__ == "__main__":
    main()
