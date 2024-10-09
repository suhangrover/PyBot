import tkinter as tk
from tkinter import ttk, messagebox
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat
import pyttsx3

# Initialize the AI21 client
client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Define chatbot roles
roles = {
    "general": "You are a helpful assistant.",
    "therapist": "You are a compassionate therapist who helps users with mental well-being."
}

conversation_history = []  # Store conversation history

# Function to set the chatbot's role dynamically
def set_role(role):
    global current_role
    current_role = roles.get(role, roles["general"])
    conversation_box.insert(tk.END, f"Bot role set to: {role.capitalize()}\n", "bot")

# Handle general conversation
def handle_general_conversation(user_input):
    general_responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help?",
        "how are you": "I'm just a chatbot, but I'm here to assist you!",
        "who are you": f"I am your {current_role.lower().split()[1]}, ready to assist you.",
        "what is your purpose": f"My role is to {current_role.lower()}.",
        "bye": "Goodbye! Have a great day!",
        "thanks": "You're welcome!",
    }

    normalized_input = user_input.lower().strip()
    return general_responses.get(normalized_input, None)

# Suggest helpful resources based on keywords
def suggest_resources(user_input):
    resource_keywords = {
        "stress": "https://www.helpguide.org/articles/stress/stress-management.htm",
        "anxiety": "https://www.anxiety.org/",
        "depression": "https://www.nimh.nih.gov/health/topics/depression",
        "self-care": "https://www.mind.org.uk/information-support/tips-for-everyday-living/wellbeing/self-care/",
        "productivity": "https://www.lifehack.org/articles/productivity",
    }

    suggestions = []
    for keyword, link in resource_keywords.items():
        if keyword in user_input.lower():
            suggestions.append(f"For more on {keyword}, check this out: {link}")
    
    return "\n".join(suggestions)

# Get chatbot response
def get_bot_response():
    user_input = entry.get()

    if user_input.lower() in ["exit", "quit"]:
        conversation_box.insert(tk.END, "Bot: Goodbye!\n", "bot")
        root.quit()
        return

    # Insert user input to conversation box
    conversation_box.insert(tk.END, f"You: {user_input}\n", "user")
    conversation_history.append(f"You: {user_input}\n")

    # Handle general conversation first
    general_response = handle_general_conversation(user_input)

    if general_response:
        # Display the general response first, then convert it to speech
        conversation_box.insert(tk.END, f"Bot: {general_response}\n", "bot")
        conversation_history.append(f"Bot: {general_response}\n")
        entry.delete(0, tk.END)  # Clear the entry field
        conversation_box.see(tk.END)  # Scroll down to the latest message
        root.after(200, lambda: speak_text(general_response))  # Delay to allow the text to appear before speech
    else:
        # Prepare the conversation prompt based on the current role
        prompt = f"""
        Context: {current_role}
        User's Input: {user_input}
        """
        
        messages = [
            ChatMessage(role="system", content=current_role),
            ChatMessage(role="user", content=prompt)
        ]

        # Error handling for API request
        try:
            response = client.chat.completions.create(
                model="jamba-instruct",
                messages=messages,
                n=1,
                max_tokens=1024,
                temperature=0.7,
                response_format=ResponseFormat(type="text"),
            )
            assistant_response = response.choices[0].message.content
            
            # Display assistant response first, then convert it to speech
            conversation_box.insert(tk.END, f"Bot: {assistant_response}\n", "bot")
            conversation_history.append(f"Bot: {assistant_response}\n")
            entry.delete(0, tk.END)
            conversation_box.see(tk.END)  # Scroll to the latest message
            root.after(200, lambda: speak_text(assistant_response))  # Delay for speech
        except Exception as e:
            conversation_box.insert(tk.END, "Bot: Sorry, there was an error in processing your request.\n", "bot")

    # Suggest helpful resources
    suggestions = suggest_resources(user_input)
    if suggestions:
        conversation_box.insert(tk.END, f"Bot: {suggestions}\n", "bot")

# Clear the conversation history
def clear_conversation():
    conversation_box.delete(1.0, tk.END)
    conversation_history.clear()
    conversation_box.insert(tk.END, "Conversation cleared.\n", "bot")

# Save conversation history to a file
def save_conversation():
    with open("conversation_history.txt", "w") as file:
        for line in conversation_history:
            file.write(line)
    messagebox.showinfo("Save", "Conversation history saved successfully!")

# GUI improvements
root = tk.Tk()
root.title("AI21 Chatbot - Byte Club")
root.geometry("700x600")  # Initial size
root.resizable(True, True)  # Allow window resizing
root.configure(bg="#1e1e2f")

FONT = ("Helvetica", 12)
USER_FONT = ("Helvetica", 12, "bold")
BOT_FONT = ("Helvetica", 12)

# Frame for conversation box
conversation_frame = tk.Frame(root, bg="#1e1e2f")
conversation_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add scroll bar to the conversation box
scrollbar = tk.Scrollbar(conversation_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for conversation history
conversation_box = tk.Text(conversation_frame, wrap='word', font=FONT, fg="#F0F0F0", bg="#2c2c34", yscrollcommand=scrollbar.set)
conversation_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=conversation_box.yview)

# Configure text tags
conversation_box.tag_configure("user", foreground="#56dbab", font=USER_FONT)
conversation_box.tag_configure("bot", foreground="#f1c40f", font=BOT_FONT)

# Frame for user input
entry_frame = tk.Frame(root, bg="#1e1e2f")
entry_frame.pack(pady=10, padx=10, fill=tk.X)

# Entry widget for user input
entry = tk.Entry(entry_frame, font=FONT, bg="#2c2c34", fg="#F0F0F0", insertbackground="white")
entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# Send button
send_button = ttk.Button(entry_frame, text="Send", command=get_bot_response, style="SendButton.TButton")
send_button.pack(side=tk.RIGHT, padx=10)

# Dropdown to change chatbot's role
role_var = tk.StringVar(value="general")
role_dropdown = ttk.OptionMenu(root, role_var, "general", "general", "therapist", command=set_role)
role_dropdown.pack(pady=10)

# Clear and save buttons
clear_button = ttk.Button(root, text="Clear Conversation", command=clear_conversation, style="SendButton.TButton")
clear_button.pack(pady=5)

save_button = ttk.Button(root, text="Save Conversation", command=save_conversation, style="SendButton.TButton")
save_button.pack(pady=5)

# Styling for buttons
style = ttk.Style()
style.configure("SendButton.TButton", font=("Helvetica", 10), padding=10, background="#3e3e52", foreground="#000000")  # Set text color to black
style.map("SendButton.TButton", background=[('active', '#565675')])

# Bind Enter key to send button
root.bind('<Return>', lambda event: get_bot_response())

# Set default role
current_role = roles["general"]
set_role("general")

# Start the GUI loop
root.mainloop()
