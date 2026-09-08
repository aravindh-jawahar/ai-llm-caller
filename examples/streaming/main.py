"""Streaming: print tokens as they arrive instead of waiting for the full reply.

Same call as llm_basics, but with `stream=True`. The response arrives in small
chunks; we print each chunk's text as soon as we get it.
"""

from core.providers import get_client, get_model


def run() -> None:
    client = get_client()
    model = get_model()

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Write a short, upbeat poem about learning to code with AI.",
            }
        ],
        temperature=0.9,
        stream=True,
    )

    # Each chunk carries a small piece of the reply in `delta.content`.
    # Some chunks have no choices at all (e.g. a final usage-only chunk), and
    # `delta.content` can be None, so we guard against both.
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()  # final newline once the stream ends


if __name__ == "__main__":
    run()
