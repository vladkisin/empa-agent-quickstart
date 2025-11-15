from agents.graph import create_graph


def main():
    graph = create_graph()
    user_id = "demo_user"

    while True:
        msg = input("You: ")
        if not msg:
            break

        state = {
            "user_id": user_id,
            "user_message": msg,
        }
        result = graph.invoke(state)
        print("Agent:", result.get("response", ""))


if __name__ == "__main__":
    main()

