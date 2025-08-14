# main.py
from typing import Dict, Any
from personas import personalize_personas  # uses your pasted STORIES internally
from dialog import generate_chat_turn

def create_initial_state() -> Dict[str, Any]:
    return {
        "current_name": None,  # set after /pick
        "nsfw": False,         # default OFF; toggle with /nsfw_on
    }

def main():
    # ensure personas are hydrated with memories/favorites
    try:
        personalize_personas(state=None)
    except Exception:
        # personas.py may not need state; ignore
        pass

    state = create_initial_state()
    print("Chat ready. Type /help for commands.\n")

    while True:
        try:
            user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user:
            continue
        if user.lower() in ("/quit", "/exit"):
            print("Bye!")
            break

        reply = generate_chat_turn(state, user)
        print(reply, flush=True)

if __name__ == "__main__":
    main()