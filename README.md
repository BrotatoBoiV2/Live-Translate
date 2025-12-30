# Live Translate

Live Translate is a near-real-time translation application that uses WebRTC VAD and Whisper to translate audio in real-time.

---

## Prerequisites
Before installing, you may need to make sure you have installed the following system libraries for audio handling:

**Ubuntu/Debian**
```bash
sudo apt-get install libportaudio2 libportaudio-dev portaudio19-dev
```

**Fedora**
```bash
sudo dnf install portaudio portaudio-devel
```

**macOS**
```bash
brew install portaudio
```

## Installation
**1. Clone and Enter the Repository**
```bash
git clone https://github.com/BrotatoBoiV2/Live-Translate.git
cd Live-Translate
```

**2. Create and Activate a Virtual Environment**
```bash
python -m venv ./env
# Windows
.\env\Scripts\activate
# Linux/Mac
source ./env/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```
**4. Open `main.py` and modify the device index to match your audio device.**:
You can find what index number your device is by running the following command `python -m sounddevice` - available after running `pip install -r requirements.txt`.
**5. Run the Program**
```bash
python main.py
```

---

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Documentation

You can find the documentation for this project in the [DOCUMENTATION.md](DOCUMENTATION.md) file.


## Important Acknowledgments
This project was created by a human and refined with the help of AI tools.

The following repos made this project possible:
- [WebRTC VAD](https://github.com/wiseman/py-webrtcvad)
- [Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/cybertronai/faster-whisper)
