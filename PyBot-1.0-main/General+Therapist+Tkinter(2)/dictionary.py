import tkinter as tk
from tkinter import ttk
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat

# Initialize the AI21 client
client = AI21Client(api_key="F0vMbwgybEVr0EmoKFXunpNjLHrqMXVT")

# Define chatbot roles
roles = {
    "general": "You are a helpful assistant.",
    "therapist": "You are a compassionate therapist who helps users with mental well-being."
}

# Function to set the chatbot's role dynamically
def set_role(role):
    global current_role
    current_role = roles.get(role, roles["general"])
    conversation_box.insert(tk.END, f"Bot role set to: {role.capitalize()}\n", "bot")

# Handle therapy-related conversation
def handle_therapy_conversation(user_input):
    therapy_keywords = [
    # Anxiety-related
    "anxiety", "stress", "nervousness", "worry", "apprehension", "panic", 
    "fear", "phobia", "restlessness", 

    # Depression-related
    "depression", "depressed", "sadness", "melancholy", "low mood", 
    "hopelessness", "despair", "feeling down", "feeling blue", 
    "emptiness", 

    # Trauma-related
    "trauma", "PTSD", "flashbacks", "nightmares", "post-traumatic stress", 
    "abuse", "emotional trauma", "childhood trauma", "distress", 

    # Grief and Loss
    "grief", "mourning", "bereavement", "loss", "heartache", "sorrow", 
    "crying", 

    # Self-esteem and Confidence
    "self-esteem", "self-doubt", "low self-esteem", "insecurity", 
    "lack of confidence", 

    # Relationships and Conflict
    "relationship issues", "family conflict", "trust issues", 
    "communication problems", "marital problems", "boundaries", 
    "divorce", "breakup", 

    # Emotional regulation and coping
    "emotional pain", "emotional regulation", "anger", "frustration", 
    "irritability", "mood swings", "emotional outbursts", "resentment", 

    # Burnout and Overwhelm
    "overwhelmed", "burnout", "fatigue", "exhaustion", "mental exhaustion", 
    "feeling drained", "lack of energy", 

    # Personal development and self-care
    "self-care", "self-compassion", "healing", "inner peace", "balance", 
    "resilience", "mindfulness", "personal growth", "empathy", "compassion", 

    # Negative thoughts and mental health challenges
    "negative thoughts", "intrusive thoughts", "self-criticism", "self-blame", 
    "shame", "guilt", "vulnerability", "existential crisis", "identity crisis", 

    # Miscellaneous
    "isolation", "loneliness", "social anxiety", "insomnia", "forgiveness", 
    "life changes", "coping", "mental well-being", "emotional support", 
    "counseling", "therapy", "insecure"
]

    
    for keyword in therapy_keywords:
        if keyword in user_input.lower():
            return True
    return False

# Handle general conversation
def handle_general_conversation(user_input):
    general_responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help?",
        "how are you": "I'm just a chatbot, but I'm here to assist you!",
        "who are you": f"I am your {current_role.lower().split()[1]}, ready to assist you.",
        "what is your purpose": f"My role is to {current_role.lower()}.",
        "bye": "Goodbye! Have a great day!",
        "thanks": "You're welcome!"
    }

    normalized_input = user_input.lower().strip()
    return general_responses.get(normalized_input, None)

# Get chatbot response
def get_bot_response():
    user_input = entry.get()

    if user_input.lower() in ["exit", "quit"]:
        conversation_box.insert(tk.END, "Bot: Goodbye!\n", "bot")
        root.quit()
        return

    conversation_box.insert(tk.END, f"You: {user_input}\n", "user")
    
    # Check if in therapist mode and restrict to therapy questions
    if current_role == roles["therapist"]:
        if not handle_therapy_conversation(user_input):
            conversation_box.insert(tk.END, "Bot: I'm here to help with therapy-related topics only. Let's talk about how you're feeling.\n", "bot")
            entry.delete(0, tk.END)
            return
    
    # Handle general conversation
    general_response = handle_general_conversation(user_input)
    
    if general_response:
        conversation_box.insert(tk.END, f"Bot: {general_response}\n", "bot")
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

        # Send request to AI21 model
        response = client.chat.completions.create(
            model="jamba-1.5-large",
            messages=messages,
            n=1,
            max_tokens=1024,
            temperature=0.7,
            response_format=ResponseFormat(type="text"),
        )

        assistant_response = response.choices[0].message.content
        conversation_box.insert(tk.END, f"Bot: {assistant_response}\n", "bot")
    
    entry.delete(0, tk.END)

# GUI improvements
root = tk.Tk()
root.title("AI21 Chatbot - Adaptive Assistant")
root.geometry("700x600")
root.resizable(False, False)
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
conversation_box = tk.Text(conversation_frame, wrap='word', height=20, width=60, font=FONT, fg="#F0F0F0", bg="#2c2c34", yscrollcommand=scrollbar.set)
conversation_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=conversation_box.yview)

# Configure text tags
conversation_box.tag_configure("user", foreground="#56dbab", font=USER_FONT)
conversation_box.tag_configure("bot", foreground="#f1c40f", font=BOT_FONT)

# Frame for user input
entry_frame = tk.Frame(root, bg="#1e1e2f")
entry_frame.pack(pady=10, padx=10, fill=tk.X)

# Entry widget for user input
entry = tk.Entry(entry_frame, width=40, font=FONT, bg="#2c2c34", fg="#F0F0F0", insertbackground="white")
entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# Send button
send_button = ttk.Button(entry_frame, text="Send", command=get_bot_response, style="SendButton.TButton")
send_button.pack(side=tk.RIGHT, padx=10)

# Dropdown to change chatbot's role
role_var = tk.StringVar(value="general")
role_dropdown = ttk.OptionMenu(root, role_var, "general", "general", "therapist", command=set_role)
role_dropdown.pack(pady=10)

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
