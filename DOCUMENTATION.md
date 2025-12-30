# Documentation: Live Translate
**1. Technical Overview**

Live Translate operates on a producer-consumer model using three main components:
    Audio Ingest (Producer): Captures high-sample-rate audio and downsamples it.
    VAD Gatekeeper: Analyzes audio chunks to determine if speech is occurring.
    Inference Engine (Consumer): Translates the captured speech using Faster-Whisper.

**2. Signal Processing (audio_stream.py)**

To ensure compatibility with WebRTC VAD and Whisper, the audio must be exactly 16,000 Hz.
    Resampling: We capture at 44,100 Hz (standard hardware rate) and use scipy.signal.resample_poly with a ratio of 160/441 to reach 16,000 Hz.
    Precision: Capturing is done in float32 to avoid quantization errors during the math phase, then clipped and cast to int16 for the VAD.

**3. Voice Activity Detection (vad_module.py)**

We use a 30ms window size (480 samples at 16kHz) because WebRTC VAD strictly requires 10, 20, or 30ms frames.
    Pre-roll: Stores the 300ms of audio before speech was detected to ensure the start of the first word isn't clipped.
    Post-roll: Waits for 510ms of silence before declaring a "phrase" complete. This allows for natural pauses between words.

**4. Translation Logic (translate.py)**

The system uses the Whisper-small model with the following optimizations:
    Task: translate (Foreign → English).
    English Gate: If the detected language is en, the output is discarded to prevent redundancy.
    Hallucination Filter: Any segment with a no_speech_prob greater than 0.6 is ignored.

# Developer Journal (UTC)

2025-12-30

    16:52
        Created the base version of the program.
        Status: Core logic is functional. Resampling and VAD gatekeeping are stable.
        Observation: Translations are functional, but accuracy is limited by CPU-bound inference speed on small model.
    
    20:33
        Cleaned and refactored the code.
        Status: Need to test the Cleaned and Refactored code before I push to the main branch.

# Future Roadmap (TODO)

    [ ] Internal Audio Input: Implement Loopback support (e.g., via PyCURL or specialized sounddevice settings) to translate desktop audio instead of just the microphone.
    [ ] GUI: Transition from CLI to a transparent overlay for live subtitling.