from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat

client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")  # Your API key here

while True:
    # Ask the user for input in the terminal
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye")
        break
    
    messages = [
        ChatMessage(
            role="user",
            content=user_input
        )
    ]

    response = client.chat.completions.create(
        model="jamba-1.5-large",
        messages=messages,
        documents=[],
        tools=[],
        n=1,
        max_tokens=1024,
        temperature=0.4,
        top_p=1,
        stop=[],
        response_format=ResponseFormat(type="text"),
    )

    assistant_response = response.choices[0].message.content
    print(f"Bot: {assistant_response}")