from faster_whisper import WhisperModel
import numpy as np

class Translator:
    def __init__(self):
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

    def transcribe_chunk(self, audio_bytes):
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        segments, info = self.model.transcribe(audio_np, task="translate", beam_size=1) # ~ Transcribe the audio. ~ #
        
        if info.language == "en":
            return None, None
        
        text = "".join([segment.text for segment in segments]) # ~ Join the segments into a single string. ~ #

        return text.strip(), info.language # ~ Return the text and the language. ~ #
