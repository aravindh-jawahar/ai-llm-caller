"""LLM basics: a single request, a single response.

The simplest possible LLM interaction — send one message, print the reply.
Start here.
"""

from core.providers import get_client, get_model


def run() -> None:
    client = get_client()
    model = get_model()

    # chat.completions is the universal OpenAI-compatible endpoint: the same
    # code works across NVIDIA, OpenAI, and Ollama.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who provides clear and concise explanations. You are specialised in Finance",
            },
            {
                "role": "user",
                "content": "Explain what is a share market vs Stock vs bond market",
            }
        ],
        temperature=0.7,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    run()
