import sys
import os
from pytubefix import YouTube
from common import download_audio, transcribe_audio, clean_up


def youtube_downloader(url, output_path):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(
        output_path=os.path.dirname(output_path),
        filename=os.path.basename(output_path) + ".mp3",
    )
    return audio_file


def main(url):
    temp_audio = "temp_audio"

    try:
        audio_file = download_audio(url, temp_audio, youtube_downloader)
        if not audio_file:
            print("Failed to download audio.")
            return

        transcript = transcribe_audio(audio_file)
        print(transcript)

    finally:
        clean_up(temp_audio)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python youtube_to_text.py <YouTube_URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    main(youtube_url)
