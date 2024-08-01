import sys
import whisper
import os
from pytubefix import YouTube
import yaml


def download_audio(url, output_path):
    try:
        yt = YouTube(url)

        audio_file = yt.streams.get_audio_only().download(
            output_path=os.path.dirname(output_path),
            filename=os.path.basename(output_path),
            mp3=True,
        )

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
        print("Usage: python youtube_to_text.py <YouTube_URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    main(youtube_url)
