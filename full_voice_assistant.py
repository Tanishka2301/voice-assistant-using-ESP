import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper
from google import genai
import pyttsx3

# ============================================================
# GEMINI
# ============================================================

client = genai.Client(api_key="")   # put your api key

# ============================================================
# WHISPER
# ============================================================

print("Loading Whisper...")
model = whisper.load_model("base")
print("Whisper is ready!")

# ============================================================
# TEXT TO SPEECH
# ============================================================

engine = pyttsx3.init()

# ============================================================
# AUDIO SETTINGS
# ============================================================

sample_rate = 16000

block_duration = 0.1
block_size = int(sample_rate * block_duration)

threshold = 500

silence_limit = 5.0
silence_blocks_needed = int(silence_limit / block_duration)

# ============================================================
# MAIN ASSISTANT
# ============================================================

while True:

    print("\n--------------------------------")
    print("Waiting for your voice...")
    print("--------------------------------")

    recorded_audio = []

    voice_started = False
    silence_blocks = 0

    # ========================================================
    # WAIT FOR VOICE + RECORD
    # ========================================================

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        blocksize=block_size
    ) as stream:

        while True:

            audio, overflowed = stream.read(block_size)

            volume = np.max(np.abs(audio))

            # ------------------------------------------------
            # WAITING FOR VOICE
            # ------------------------------------------------

            if not voice_started:

                if volume > threshold:

                    print("VOICE DETECTED!")
                    print("Recording started...\n")

                    voice_started = True

                    recorded_audio.append(audio.copy())

                continue

            # ------------------------------------------------
            # RECORDING
            # ------------------------------------------------

            recorded_audio.append(audio.copy())

            if volume > threshold:

                # Person is speaking
                silence_blocks = 0

            else:

                # Silence
                silence_blocks += 1

                silence_time = silence_blocks * block_duration

                print(
                    f"Silence: {silence_time:.1f} / "
                    f"{silence_limit:.1f} seconds"
                )

                # ------------------------------------------------
                # STOP AFTER 5 SECONDS OF SILENCE
                # ------------------------------------------------

                if silence_blocks >= silence_blocks_needed:

                    print("\n5 seconds of silence detected.")
                    print("Recording stopped.")

                    break

    # ========================================================
    # SAVE RECORDING
    # ========================================================

    audio_data = np.concatenate(recorded_audio)

    write(
        "recording.wav",
        sample_rate,
        audio_data
    )

    print("\nSaved as: recording.wav")

    # ========================================================
    # WHISPER: SPEECH → TEXT
    # ========================================================

    print("\nConverting speech to text...")

    result = model.transcribe("recording.wav")

    question = result["text"].strip()

    print("\nYou said:")
    print(question)

    # ========================================================
    # EXIT COMMAND
    # ========================================================

    if question.lower() in ["exit", "quit", "stop"]:

        print("\nGoodbye!")

        break

    # ========================================================
    # GEMINI
    # ========================================================

    print("\nGemini is thinking...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question
    )

    answer = response.text

    print("\nGemini:") 
    print(answer)

# Remove Markdown formatting before speaking
    spoken_answer = answer.replace("*", "")
    spoken_answer = spoken_answer.replace("#", "")
    spoken_answer = spoken_answer.replace("_", "")
    spoken_answer = spoken_answer.replace("`", "")

    print("\nSpeaking...")
    engine.say(spoken_answer)
    engine.runAndWait()
    print("Finished.")   
    # TEXT → SPEECH
    # ========================================================
AQ.Ab8RN6K4RnqXs4KYSQ3wRtexsB-C2uxkWoStR5hw6O40B9UNJA
