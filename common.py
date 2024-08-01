import os
import whisper
import yaml


def download_audio(url, output_path, downloader):
    try:
        audio_file = downloader(url, output_path)
        return audio_file
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None


def transcribe_audio(audio_path):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    model = whisper.load_model(config["whisper"]["model_size"])
    result = model.transcribe(audio_path)
    return result["text"]


def clean_up(file_path):
    if os.path.exists(file_path + ".mp3"):
        os.remove(file_path + ".mp3")
