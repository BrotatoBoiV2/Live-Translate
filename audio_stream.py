"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Live Translate.
   Description: A live translating application using WebRTC VAD and Whisper.
                              File: audio_stream.py
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


import sounddevice as sd
from scipy import signal
import numpy as np
import queue
import sys


class AudioStream:
    def __init__(self, device_index=None, rate=48000, chunk_ms=30):
        self.rate = rate
        self.target_rate = 16000
        self.chunk_size = int(rate * chunk_ms / 1000)
        self.audio_queue = queue.Queue()
        self.device_index = device_index
        self.stream = None
        self._is_running = False

    def get_resampled_chunk(self):
        """
            Fetches 44.1k data and returns 16k datafor VAD/Whisper.
        """

        raw_data_bytes = self.audio_queue.get()
        audio_np = np.frombuffer(raw_data_bytes, dtype=np.int16)
        resampled = signal.resample_poly(audio_np, 160, 441)
        resampled = indata[::3, 0]
        resampled_int16 = resampled.astype(np.int16)

        return resampled_int16[:480].tobytes()

    def _callback(self, indata, frames, time, status):
        """
            This runs in a high-priority background thread.
        """

        if status:
            if "overflow" in str(status):
                sys.stderr.write('.')
                sys.stderr.flush()
            
        data = (indata[:, 0] * 2.0).clip(-32768, 32767).astype(np.int16)
        indices = np.linspace(0, len(data) - 1, 480)
        resampled = indata[::3, 0]

        self.audio_queue.put(resampled.astype(np.int16).tobytes())
    
    def start(self):
        if self._is_running:
            return

        # ~ Factual Check: If no device is provided, use the system default. ~ #
        if self.device_index is None:
            self.device_index = sd.default.device[0]

        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=1,
            dtype='int16',  # ~ Standard for WebRTC VAD and Whisper. ~ #
            blocksize=self.chunk_size,
            device=self.device_index,
            callback=self._callback,
        )
        
        self.stream.start()
        self._is_running = True

        print(f"Audio stream has been started on device {self.device_index}.")
        print(f"Audio stream is running at {self.rate} Hz with a chunk size of {self.chunk_size} samples.")

    def get_next_chunk(self):
        """
            Fetche a chunk from the queue.
            This will wait until data is available.
        """

        return self.audio_queue.get()

    def stop(self):
        if self._is_running:
            self.stream.stop()
            self.stream.close()
            self._is_running = False

            print("Audio stream has been stopped.")
        
