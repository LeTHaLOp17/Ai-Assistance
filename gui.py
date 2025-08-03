import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

from tts import speak
from ai_client import get_ai_response, smart_speak  # Import smart_speak as well!
from speech_rec import streaming_recognize_speech
import re

class ZoroGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZORO AI Assistant")
        self.geometry("700x450")
        
        self.transcript = ScrolledText(self, state="disabled", wrap=tk.WORD, font=("Arial", 13))
        self.transcript.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listen_btn = tk.Button(self, text="🎤 Start Listening", command=self.listen_thread, font=("Arial", 12))
        self.listen_btn.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def listen_thread(self):
        self.listen_btn.config(state="disabled", text="Listening...")
        thread = threading.Thread(target=self.handle_voice_query)
        thread.start()

    def handle_voice_query(self):
        try:
            user_text = streaming_recognize_speech()
            self.display(f"\n👤 You: {user_text}\n\n", "user")
            ai_reply = get_ai_response(user_text)
            # Extract and handle conversational reply and output block separately
            voice_reply, output_block = self.parse_ai_reply(ai_reply)
            self.display(f"🤖 ZORO: {voice_reply}\n", "zoro")
            if output_block:
                self.display(f"\n[Output Block]\n{output_block}\n\n", "output")
            speak(voice_reply)
        except Exception as e:
            self.display(f"Error: {e}\n", "error")
        finally:
            self.listen_btn.config(state="normal", text="🎤 Start Listening")

    def parse_ai_reply(self, ai_text):
        """
        Split reply into conversational line (for speaking) and output block (for screen).
        Matches your smart_speak() logic.
        """
        # Split triple single quotes blocks
        # Both '''...''' and rest as natural text
        split_blocks = re.split(r"'''(.*?)'''", ai_text, flags=re.DOTALL)
        voice_reply = ""
        output_block = ""
        for idx, part in enumerate(split_blocks):
            if idx % 2 == 1 and part.strip():
                output_block += part.strip() + "\n"
            elif idx == 0 and part.strip():
                voice_reply = part.strip()
        # Fallback if nothing found
        if not voice_reply:
            voice_reply = "Boss, output screen par dikha diya hai!"
        # Clean up voice reply (just in case)
        if len(voice_reply.split()) > 35:
            voice_reply = " ".join(voice_reply.split()[:35]) + " ... aur baaki screen pe check karo!"
        return voice_reply, output_block

    def display(self, message, tag=None):
        self.transcript.configure(state="normal")
        self.transcript.insert(tk.END, message)
        self.transcript.configure(state="disabled")
        self.transcript.see(tk.END)

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    app = ZoroGUI()
    app.mainloop()
