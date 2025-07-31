import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import threading

# Import your existing functions from your modules
from memory import load_memory, save_memory
from ai_client import get_ai_response
from tts import speak

class AIAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")

        # Conversation display (scrollable)
        self.conversation = scrolledtext.ScrolledText(root, state='disabled', width=70, height=20, wrap=tk.WORD)
        self.conversation.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input box
        self.user_input = tk.Entry(root, width=60)
        self.user_input.grid(row=1, column=0, padx=10, sticky='w')
        self.user_input.bind("<Return>", self.send_input)  # Send on Enter key

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_input)
        self.send_button.grid(row=1, column=1, padx=10, pady=5, sticky='e')

        # Load memory once
        self.memory = load_memory()

    def append_text(self, text, sender="AI"):
        self.conversation.config(state='normal')
        if sender == "User":
            self.conversation.insert(tk.END, f"You: {text}\n")
        else:
            self.conversation.insert(tk.END, f"AI: {text}\n")
        self.conversation.config(state='disabled')
        self.conversation.see(tk.END)  # Scroll to bottom

    def send_input(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return  # Ignore empty input

        self.append_text(user_text, sender="User")
        self.user_input.delete(0, tk.END)

        # Run AI response in a separate thread to avoid freezing GUI
        threading.Thread(target=self.handle_query, args=(user_text,), daemon=True).start()

    def handle_query(self, user_input):
        user_lower = user_input.lower()

        # Handle exit commands
        if user_lower in ['exit', 'quit']:
            self.append_text("Goodbye! Closing the assistant.", sender="AI")
            self.root.quit()
            return

        # Handle remember command
        if user_lower.startswith("remember ") and " is " in user_lower:
            try:
                rest = user_input[8:]
                key, value = rest.split(" is ", 1)
                key = key.strip().lower()
                value = value.strip()
                self.memory[key] = value
                save_memory(self.memory)
                response = f"Okay, I will remember {key} is {value}."
                self.append_text(response)
                speak(response)
                return
            except Exception:
                error_msg = "Sorry, please say it like 'remember X is Y'."
                self.append_text(error_msg)
                speak(error_msg)
                return

        # Handle what is command
        if user_lower.startswith("what is "):
            key = user_lower[8:].strip()
            if key in self.memory:
                response = f"{key} is {self.memory[key]}"
            else:
                response = f"I don't know what {key} is yet. You can teach me by saying 'remember {key} is ...'"
            self.append_text(response)
            speak(response)
            return

        # Otherwise ask AI model
        try:
            response = get_ai_response(user_input)
            self.append_text(response)
            speak(response)
        except Exception as e:
            error_msg = f"Error: {e}"
            self.append_text(error_msg)
            speak(error_msg)

def run_gui():
    root = tk.Tk()
    app = AIAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
# gui.py - A simple GUI for the AI Assistant
# This file provides a graphical interface for interacting with the AI assistant.
# It allows users to input queries, view conversation history, and manage memory.