from agents.graph import create_graph
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(message)s'
)

def main():
    app = create_graph()
    user_id = "demo_user"
    config = {"configurable": {"thread_id": user_id}}

    print("=" * 60)
    print("OneHabit supervisor demo - Multi-turn conversation")
    print("Empty line to exit, 'reset' to clear conversation")
    print("=" * 60)
    print()

    turn = 1

    while True:
        msg = input(f"\n[Turn {turn}] You: ")
        if not msg.strip():
            break
        
        if msg.strip().lower() == "reset":
            import uuid
            user_id = f"demo_user_{uuid.uuid4().hex[:8]}"
            config = {"configurable": {"thread_id": user_id}}
            turn = 1
            print("\n[Conversation reset]")
            continue

        print(f"\n{'='*60}")
        print(f"TURN {turn} - Processing...")
        print(f"{'='*60}")

        try:
            current_state = app.get_state(config)
            if current_state.values:
                existing_messages = current_state.values.get("messages", [])
                print(f"[DEBUG] Current conversation has {len(existing_messages)} messages")
            else:
                existing_messages = []
                print("[DEBUG] Starting new conversation")
        except Exception:
            existing_messages = []
            print("[DEBUG] Starting new conversation")

        result = app.invoke(
            {
                "user_id": user_id,
                "user_message": msg,
            },
            config=config
        )
        
        print(f"\n{'='*60}")
        print("RESPONSE:")
        print(f"{'='*60}")
        print(result.get("response", ""))
        print()
        
        all_messages = result.get("messages", [])
        print(f"[DEBUG] Total messages in conversation: {len(all_messages)}")
        
        turn += 1

if __name__ == "__main__":
    main()

