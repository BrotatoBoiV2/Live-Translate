"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Live Translate.
   Description: A live translating application using WebRTC VAD and Whisper.
                           File: translate.py
                            Date: 2025/12/30
                        Version: 1.0-2025.12.30

===============================================================================

                        Copyright (C) 2025 BrotatoBoi

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as published
        by the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.

        You should have received a copy of the GNU Affero General Public License
        along with this program. If not, see <https://www.gnu.org/licenses/>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# ~ Import Third-Party Modules. ~ #
from faster_whisper import WhisperModel
import numpy as np


class Translator:
    """
        This class handles the translation of audio chunks.

        Functions:
            __init__
            transcribe_chunk
    """

    def __init__(self):
        """
            Initializes the Translator class.

            Attributes:
                model (WhisperModel): The Whisper model used for translation.
        """

        self.model = WhisperModel("small", device="cpu", compute_type="int8")

    def transcribe_chunk(self, audio_bytes):
        """
            Transcribes an audio chunk and returns the text and language if it is not English.

            Args:
                audio_bytes (bytes): The audio chunk to transcribe.

            Returns:
                text (str): The transcribed text.
                lang (str): The detected language.
        """

        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        segments, info = self.model.transcribe(audio_np, task="translate", beam_size=1)
        
        if info.language == "en":
            return None, None
        
        text = "".join([segment.text for segment in segments])

        return text.strip(), info.language
