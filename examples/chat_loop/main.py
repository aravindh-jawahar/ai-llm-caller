"""Chat loop: a multi-turn conversation that remembers context.

The model itself is stateless — it "remembers" only because we resend the full
message history on every turn. This example keeps that history in a list and
streams each reply.
"""

from core.providers import get_client, get_model

EXIT_WORDS = {"exit", "quit"}


def run() -> None:
    client = get_client()
    model = get_model()

    # The running conversation. The system message sets the assistant's behavior.
    messages: list[dict] = [
        {"role": "system", "content": "You are a concise, friendly assistant."}
    ]

    print("Chat with the model. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.lower() in EXIT_WORDS:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        print("ai> ", end="", flush=True)
        reply_parts: list[str] = []
        for chunk in stream:
            if not chunk.choices:
                continue  # e.g. a final usage-only chunk carries no choices
            delta = chunk.choices[0].delta.content
            if delta:
                reply_parts.append(delta)
                print(delta, end="", flush=True)
        print("\n")

        # Append the assistant's reply so the next turn has full context.
        messages.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    run()
