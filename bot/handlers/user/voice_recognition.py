import whisper
from pydub import AudioSegment
import numpy as np

# Load Whisper model
model = whisper.load_model("tiny")

audio_path = "/home/alim/Downloads/sample.ogg"

# Load your audio file (assume .ogg or another compatible format)
audio = AudioSegment.from_file(audio_path, format="ogg")

# Define chunk duration (30 seconds in milliseconds)
chunk_duration = 30 * 1000

# Split audio into 30-second chunks
chunks = [audio[i:i + chunk_duration] for i in range(0, len(audio), chunk_duration)]

# Initialize transcription
full_transcription = ""

# Process each chunk
for i, chunk in enumerate(chunks):
    # Export chunk as wav format to load with whisper
    chunk.export("temp_chunk.wav", format="wav")
    
    # Load and process chunk with Whisper
    audio_data = whisper.load_audio("temp_chunk.wav")
    audio_data = whisper.pad_or_trim(audio_data)  # Ensure each chunk is 30s
    
    # Create Mel spectrogram and transcribe
    mel = whisper.log_mel_spectrogram(audio_data).to(model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    
    # Append the result to the full transcription
    full_transcription += result.text + " "

print("Full transcription:", full_transcription)