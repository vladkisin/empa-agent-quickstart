from agents.graph import create_graph

def main():
    app = create_graph()
    user_id = "demo_user"

    print("OneHabit supervisor demo. Empty line to exit.\n")

    while True:
        msg = input("You: ")
        if not msg.strip():
            break

        result = app.invoke(
            {
                "user_id": user_id,
                "user_message": msg,
                "messages": [],
                "response": "",
            }
        )
        print("Agent:", result.get("response", ""))

if __name__ == "__main__":
    main()

