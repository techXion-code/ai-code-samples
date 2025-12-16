import gradio as gr
import tempfile
import soundfile as sf
import wave
import json
import pyttsx3
import numpy as np

from vosk import Model, KaldiRecognizer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# --------------------------------------------
# 1. Load Hugging Face Chat Model (FREE + OFFLINE)
# --------------------------------------------
print("Loading Hugging Face model...")

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
#model_name = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chatbot = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=150,
    do_sample=True,
    temperature=0.7
)

print("Model loaded successfully!")

# --------------------------------------------
# 2. Load Vosk Speech-to-Text Model
# --------------------------------------------
vosk_model_path = r"vosk-model-small-en-us-0.15"  # UPDATE IF DIFFERENT
print("Loading Vosk model...")

vosk_model = Model(vosk_model_path)

print("Vosk loaded successfully!")

# --------------------------------------------
# 3. Offline Text-to-Speech (pyttsx3)
# --------------------------------------------
engine = pyttsx3.init()

def tts_to_audio(text):
    """Convert text into WAV audio file."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    engine.save_to_file(text, temp.name)
    engine.runAndWait()
    return temp.name

# --------------------------------------------
# 4. Convert Gradio's numpy audio → WAV
# --------------------------------------------
def convert_numpy_to_wav(audio_np, sample_rate):
    """Convert numpy array audio into a WAV file for Vosk."""
    audio_np = np.array(audio_np)

    # If audio is 1D, expand to 2D mono
    if audio_np.ndim == 1:
        audio_np = np.expand_dims(audio_np, axis=1)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio_np, sample_rate)
    print(temp_file.name)
    return temp_file.name

# --------------------------------------------
# 5. Speech-to-text using Vosk
# --------------------------------------------
def speech_to_text(wav_path):
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())

    text_result = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text_result = result.get("text", "")

    # final bits
    final = json.loads(rec.FinalResult())
    final_text = final.get("text", "")

    return final_text or text_result

# --------------------------------------------
# 6. Ask Hugging Face Chat Model
# --------------------------------------------
def ask_ai(prompt):
    raw = chatbot(prompt)[0]["generated_text"]
    reply = raw.replace(prompt, "").strip()
    return reply

# --------------------------------------------
# 7. Main Voice Agent Logic (Gradio callback)
# --------------------------------------------
def ai_voice_agent(audio):
    if audio is None:
        return "No audio detected.", None

    # Gradio Audio(type="numpy") returns a dict
   # Gradio Audio(type="numpy") returns a TUPLE: (sample_rate, audio_data_numpy_array)
    sample_rate, audio_np = audio # <--- FIX: Unpack the tuple directly

    # 1. Check if the numpy array is empty (all zeros)
    if np.all(audio_np == 0):
         print("DEBUG: Recorded NumPy array is completely silent.")
         return "Recording was silent (check mic permissions/device).", None
    
    # Convert numpy audio to WAV
    wav_path = convert_numpy_to_wav(audio_np, sample_rate)

    # Speech to text
    user_text = speech_to_text(wav_path)

    if not user_text:
        return "I could not understand you. Please speak again.", None

    print("User:", user_text)

    # AI generates reply
    ai_reply = ask_ai(user_text)
    print("AI:", ai_reply)

    # Convert reply to audio
    reply_audio_path = tts_to_audio(ai_reply)

    return ai_reply, reply_audio_path

# --------------------------------------------
# 8. Build Gradio UI
# --------------------------------------------
ui = gr.Interface(
    fn=ai_voice_agent,
    inputs=gr.Audio(
        sources=["microphone"],
        type="numpy",
        label="🎤 Speak to Your AI"
    ),
    outputs=[
        gr.Textbox(label="💬 AI Response"),
        gr.Audio(label="🔊 AI Voice Reply")
    ],
    title="AI Voice Agent (FREE, Offline)",
    description="Talk to your AI assistant! Uses Vosk STT + HuggingFace Model + pyttsx3 TTS.",
)

ui.launch()
