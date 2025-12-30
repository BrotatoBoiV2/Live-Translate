import webrtcvad
from collections import deque
import numpy as np


class VADController:
    def __init__(self, sensitivity=3):
        self.vad = webrtcvad.Vad(sensitivity)
        self.in_phrase = False
        
        # ~ Ring buffer for pre-roll: 10 chunks  * 30ms = 300ms. ~ #
        self.pre_roll = deque(maxlen=10)

        # ~ Post-roll buffer: 500ms / 30ms = 17 chunks. ~ #
        self.post_roll = 17
        self.silence_counter = 0
        self.current_phrase = []

    def process_chunk(self, chunk_bytes):
        audio_data = np.frombuffer(chunk_bytes, dtype=np.int16)
        rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))

        if rms < 500:
            is_speech = False
        else:
            is_speech = self.vad.is_speech(chunk_bytes, 16000)

        if is_speech:
            if not self.in_phrase:
                self.in_phrase = True
                self.current_phrase = list(self.pre_roll)

            self.current_phrase.append(chunk_bytes)
            self.silence_counter = 0
    
        else:
            if self.in_phrase:
                self.current_phrase.append(chunk_bytes)
                self.silence_counter += 1

                # ~ Check if the post-roll limit was hit. ~  #
                if self.silence_counter >= self.post_roll:
                    self.in_phrase = False

                    return b"".join(self.current_phrase)

            else:
                self.pre_roll.append(chunk_bytes)

        return None