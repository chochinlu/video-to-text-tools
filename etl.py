import json
import subprocess
import os
import logging
import yaml
from datetime import datetime
from tqdm import tqdm


# 設置日誌
def setup_logging():
    log_filename = f"video_etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


# 讀取配置文件
def read_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


def process_video(url, source):
    try:
        # 根據source選擇正確的腳本
        if source == "youtube":
            script = "youtube_to_text.py"
        elif source == "tiktok":
            script = "tiktok_to_text.py"
        else:
            logging.error(f"Unsupported source: {source}")
            return None

        # 呼叫對應的Python腳本
        result = subprocess.run(
            ["python", script, url], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {source} video {url}: {e}")
        return None


def main():
    setup_logging()
    config = read_config()

    input_file = config["input_file"]
    output_dir = config["output_directory"]

    logging.info("Starting ETL process")

    try:
        # 讀取JSON文件
        with open(input_file, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        return

    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)

    # 處理每個條目
    for item in tqdm(data, desc="Processing videos"):
        try:
            title = item["title"]
            url = item["url"]
            source = item["source"]

            logging.info(f"Processing: {title} from {source}")

            # 呼叫處理函數
            text = process_video(url, source)

            if text:
                # 將結果保存到文件
                filename = os.path.join(output_dir, f"{title}.txt")
                with open(filename, "w") as output_file:
                    output_file.write(text)

                logging.info(f"Saved transcript to: {filename}")
            else:
                logging.warning(f"Failed to process video: {title}")
        except KeyError as e:
            logging.error(f"Missing key in item: {e}")
        except Exception as e:
            logging.error(f"Unexpected error processing item: {e}")

    logging.info("ETL process completed")


if __name__ == "__main__":
    main()
