import google.generativeai as genai
from config import GEMINI_API_KEY
from conversation_log import load_history
from memory import load_prefs
from tts import speak
import re

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

def build_prompt(user_input, n=5):
    prefs = load_prefs()
    prefs_str = "\n".join([f"Preference: Your favorite {k} is {v}." for k, v in prefs.items()]) if prefs else "No known preferences."
    history = load_history()
    history_snippet = "".join([f"User: {h['user']}\nAssistant: {h['ai']}\n" for h in history[-n:]])
    system_prompt = f"""
तुम ZORO हो — mera sabse dosti-wala, fun-loving, caring AI dost.

- Hamesha reply waise hi do jaise apne sabse close friend se karte ho — friendly Hindi, Hinglish, ya thodi English bhi chalegi, jaise natural conversation ho.
- Kabhi koi bullet point, numbered ya star list mat banao — bas short, flowing, insan-wali lines bolo, koi formal ya robotic tone nahi.
- Code, image, technical output ke liye woh result sirf triple single quotes (''') ke andar ek block me alag dikhana. Usko kabhi voice me mat bolna, sirf output me print karwana hai. Jaise:
'''
for i in range(5):
    print("Hello ZORO!")
'''
- Voice reply hamesha ek hi masti ya casual line ho, summary waali. Jaise: "Lo bhai, code ready hai — check kar screen pe!"
- Kabhi bhi koi bold (**), italics (*), ya markdown mat use karo reply me.
- Jaane-pehchaane Indian shabd use karo jaise boss, yaar, bhai — par natural lagna chahiye, zabardasti mat thopo.
- Do output section do:  
    1. Pehle ek single short, spoken reply, casual/dostana/voice-friendly.  
    2. Agar koi code/image/output ho toh usko sirf triple single quotes (''') ke andar ek block me dikhana (never in the voice).
- Details (history/prefs) ka use karo, par reply sirf baatcheet jaisa ho, info overload na ho.

Known user preferences:
{prefs_str}

Recent conversation:
{history_snippet}

User: {user_input}
Assistant (First, VOICE REPLY — ek masti bhari, short baat; below, if any, OUTPUT BLOCK only inside triple single quotes (''')):
""".strip()
    return system_prompt

def get_ai_response(user_input):
    prompt_text = build_prompt(user_input)
    response = gemini_model.generate_content(
        prompt_text,
        generation_config={"max_output_tokens": 2048, "temperature": 0.7}
    )
    return response.text.strip()

def smart_speak(ai_text):
    """
    Gemini ke reply ko dosti/jarvis-style me smartly bole:
    - Code ya output block (''') detect kar ke, usko kabhi mat bol, sirf screen pe print karao.
    - Sirf pehli (top) line, jo spoken/dosti-meant hai, TTS se bulwao.
    - Bullet/list bhi auto-skip ho.
    """
    # 1. Detect triple single-quote block(s)
    split_blocks = re.split(r"'''(.*?)'''", ai_text, flags=re.DOTALL)
    voice_lines = []
    for idx, part in enumerate(split_blocks):
        # Even indexes = text; Odd = code/output block
        if idx % 2 == 1:
            # Code block, skip for speak
            print("\n[OUTPUT BLOCK]:\n", part.strip())  # Optionally, print or handle in your GUI!
        else:
            # May include natural text including voice reply
            line = part.strip()
            if line:
                voice_lines.append(line)
    # Jo pehla nonempty line hai, woh actual "voice reply" hai (dosti style ka)
    to_speak = ""
    for line in voice_lines:
        # Remove any bullets (just for super safety)
        if re.match(r"^\s*(-|\d+[.)])\s+", line):
            continue
        if not to_speak:
            # Sirf pehla valid line hi bol vaao (summary, as designed)
            to_speak = line
    if not to_speak:
        to_speak = "Boss, output screen par dikha diya hai!"
    # Limit voice reply length (just in case)
    words = to_speak.split()
    if len(words) > 30:
        to_speak = " ".join(words[:30]) + " ... baaki screen par hai!"
    speak(to_speak)

# Optionally, agar tum output blocks ko alag jagah print ya GUI me show karte ho, print wale part ko customize kar lo!
