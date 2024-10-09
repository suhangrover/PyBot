import tkinter as tk
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat

# Initialize AI21 client
client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")  # Your API key here

# Function to handle chat with AI21
def get_bot_response():
    user_input = entry.get()  # Get user input from the Entry widget
    
    if user_input.lower() in ["exit", "quit"]:
        conversation_box.insert(tk.END, "Bot: Goodbye\n")
        root.quit()
        return

    # Add user message to conversation box
    conversation_box.insert(tk.END, f"You: {user_input}\n")
    
    # Prepare the message for AI21
    messages = [
        ChatMessage(
            role="user",
            content=user_input
        )
    ]
    
    # Get the AI21 response
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
    
    # Add bot response to conversation box
    conversation_box.insert(tk.END, f"Bot: {assistant_response}\n")
    
    # Clear the entry field for new input
    entry.delete(0, tk.END)

# Initialize the Tkinter root window
root = tk.Tk()
root.title("AI21 Chatbot")

# Create a Text widget to display the conversation
conversation_box = tk.Text(root, wrap='word', height=20, width=50)
conversation_box.pack(padx=10, pady=10)

# Create an Entry widget for user input
entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=10)

# Create a button to send the message
send_button = tk.Button(root, text="Send", command=get_bot_response)
send_button.pack(pady=5)

# Bind the Return (Enter) key to the send button function
root.bind('<Return>', lambda event: get_bot_response())

# Run the Tkinter event loop
root.mainloop()
