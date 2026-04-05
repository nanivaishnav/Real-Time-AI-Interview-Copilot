import whisper

# Load the model (small for speed)
model = whisper.load_model("small")

def transcribe(audio_path):
    """
    audio_path: path to recorded audio
    returns: text transcription
    """
    result = model.transcribe(audio_path)
    return result["text"]