# main.py
# Main entry point for the AI assistant

import logging
from logger_setup import logging 
from memory import load_memory, save_memory  
from ai_client import get_ai_response 
from tts import speak  

def main():
    # Load saved memory (facts) before starting the assistant
    memory = load_memory()

    print("Welcome to your AI assistant (Google Gemini). Type 'exit' or 'quit' to stop.")
    logging.info("Session started.")

    while True:
        # Get user input from the console
        user_input = input("You: ").strip()
        logging.info(f"User input: {user_input}")

        # Convert input to lowercase for easier comparison
        user_input_lower = user_input.lower()

        # Exit condition: user wants to quit the program
        if user_input_lower in ["exit", "quit"]:
            print("Goodbye! Have a great day!")
            logging.info("User exited the assistant.")
            break

        # Check if the user wants the assistant to remember a fact
        # Format expected: "remember X is Y"
        if user_input_lower.startswith("remember ") and " is " in user_input_lower:
            try:
                # Extract the part after "remember "
                rest = user_input[8:]
                # Split into key and value on " is "
                key, value = rest.split(" is ", 1)
                key = key.strip().lower()  
                value = value.strip()     

                # Save fact into memory dictionary
                memory[key] = value
                # Save updated memory to file
                save_memory(memory)

                # Confirm to user that the fact was remembered
                speak(f"Okay, I will remember {key} is {value}.")
                continue  # Skip AI response this turn
            except Exception:
                # If input format is incorrect, notify user
                speak("Sorry, please say it like 'remember X is Y'.")
                continue

        # Check if the user is asking about something the assistant can remember
        # Format expected: "what is X"
        if user_input_lower.startswith("what is "):
            key = user_input_lower[8:].strip()  # Extract the key being asked about
            if key in memory:
                # If the fact exists in memory, respond with it
                speak(f"{key} is {memory[key]}")
            else:
                # If not known, prompt user to teach
                speak(f"I don't know what {key} is yet. You can teach me by saying 'remember {key} is ...'")
            continue  # Skip AI response this turn

        # For all other inputs, ask the AI model for a response
        try:
            ai_reply = get_ai_response(user_input)  # Call AI client to get reply
            logging.info(f"AI response: {ai_reply}")
            speak(ai_reply)  # Speak and print AI response
        except Exception as e:
            # Handle and log any errors calling the AI
            print(f"Error: {e}")
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
