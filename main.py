# main.py
"""
Minimal runner so everything works out of the box:

- Imports generate_chat_turn from dialog.py
- Keeps a simple REPL (type in the terminal) so you can quickly test:
    /girls
    /pick 3
    /intro
    /books
    /memory sfw
    /nsfw_on
    /memory nsfw
    /help
    /quit

If you later plug this into a web framework, you can import `generate_chat_turn`
and call it the same way with your own state management.
"""

from dialog import generate_chat_turn

def run_repl():
    print("Persona chat — type /help for commands, /quit to exit.\n")
    state = {}
    while True:
        try:
            msg = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break

        if msg.lower() in ("/quit", "/exit"):
            print("bye.")
            break

        state, reply = generate_chat_turn(state, msg)
        print(reply)

if __name__ == "__main__":
    run_repl()