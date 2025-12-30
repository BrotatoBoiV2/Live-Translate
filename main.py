"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Live Translate.
   Description: A live translating application using WebRTC VAD and Whisper.
                              File: main.py
                            Date: 2025/12/29
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


# ~ Import System Modules. ~ #
import time

# ~ Import Local Modules. ~ #
from audio_stream import AudioStream
from vad_module import VADController
from translate import Translator


def main():
    """
        The main loop for the translation program.
    """

    # ~ Initialize the audio stream, VAD, and translation engine. ~ #
    recorder = AudioStream(device_index=5)
    vad_gate = VADController()
    engine = Translator()

    recorder.start()

    print("Now recording for audio...")

    # ~ Attempt to run the main loop. ~ #
    try:
        while True:
            # ~ Get the next chunk of audio and check for phrases. ~ #
            chunk = recorder.get_next_chunk()
            phrase = vad_gate.process_chunk(chunk)

            if phrase:
                duration = len(phrase) / (16000 * 2)
                text, lang = engine.transcribe_chunk(phrase)
                
                if text:
                    print(f"Detected {lang} ({duration:.2f}s): {text}")
                else:
                    print("No speech detected.")

    except KeyboardInterrupt:
        print("\nRecording stopped by user.")

    finally:
        recorder.stop()


if __name__ == "__main__":
    main()
