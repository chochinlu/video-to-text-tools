import sys
import whisper
import os
import yaml
import pyktok as pyk
import requests


def download_audio(url, output_path):
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


def transcribe_audio(audio_path):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    model = whisper.load_model(config["whisper"]["model_size"])
    result = model.transcribe(audio_path)
    return result["text"]


def main(url):
    # 設置臨時音頻文件路徑
    temp_audio = "temp_audio"

    try:
        # 下載音頻
        audio_file = download_audio(url, temp_audio)
        if not audio_file:
            print("Failed to download audio.")
            return

        # 轉錄音頻
        transcript = transcribe_audio(audio_file)
        # 輸出轉錄文本
        print(transcript)

    finally:
        # 清理臨時文件
        if os.path.exists(temp_audio + ".mp3"):
            os.remove(temp_audio + ".mp3")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tiktok_to_text.py <Tiktok_URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    main(youtube_url)
