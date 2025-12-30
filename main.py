import time
from audio_stream import AudioStream
from vad_module import VADController
from translate import Translator


def main():
    recorder = AudioStream(device_index=5)
    vad_gate = VADController()
    engine = Translator()

    recorder.start()

    print("Now recording for audio...")

    try:
        while True:
            chunk = recorder.get_next_chunk()
            phrase = vad_gate.process_chunk(chunk)

            if phrase:
                duration = len(phrase) / (16000 * 2)
                text, lang = engine.transcribe_chunk(phrase)
                
                if text:
                    print(f"Detected {lang}: {text}")
                else:
                    print("No speech detected.")

    except KeyboardInterrupt:
        print("\nRecording stopped by user.")

    finally:
        recorder.stop()

if __name__ == "__main__":
    main()
