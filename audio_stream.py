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
        
