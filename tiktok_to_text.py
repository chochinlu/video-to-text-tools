import sys
import os
import pyktok as pyk
from common import download_audio, transcribe_audio, clean_up
import yaml
import requests


def tiktok_downloader(url, output_path):
    try:
        tt_json = pyk.alt_get_tiktok_json(url)
        audio_url = tt_json["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"][
            "itemStruct"
        ]["music"]["playUrl"]
        audio_file = requests.get(audio_url)

        with open(output_path + ".mp3", "wb") as f:
            f.write(audio_file.content)

        return os.path.abspath(output_path + ".mp3")
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None


def main(url):
    temp_audio = "temp_audio"

    try:
        audio_file = download_audio(url, temp_audio, tiktok_downloader)
        if not audio_file:
            print("Failed to download audio.")
            return

        transcript = transcribe_audio(audio_file)
        print(transcript)

    finally:
        clean_up(temp_audio)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tiktok_to_text.py <TikTok_URL>")
        sys.exit(1)

    tiktok_url = sys.argv[1]
    main(tiktok_url)
