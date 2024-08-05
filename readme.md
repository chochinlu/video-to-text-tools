# Video-to-Text Tools

Convert video voice to text, then modifiy and save it to the vector database.

## File description

`etl.py`: convert youtube / tiktok videos to texts

`copy_text.py`: just copy the texts converted from videos to the modified texts folder for manual checking.

`add_texts_to_chroma.py`: add the modified texts to the target chroma database.

`query_chroma.py`: just for validating contents in the chroma database.

`modify-texts-app.py`: a Steamlit app to help modify text converted from Whisper.

## Steps

Check the `config.yaml` config file:

```yaml
input_file: video_source.json
output_directory: texts
modified_output_directory: modified_texts
whisper:
  model_size: "large"
chromadb:
  path: "./chroma.db"
  embedding_model: "text-embedding-3-large"
  collection_name: "child_edu_2"
text_splitter:
  chunk_size: 1000
  overlap_size: 200
```

Add the API key to the `.env` file like:

```env
OPENAI_API_KEY="your api key"
```

Create a video source JSON file whose name is set in the `config.yaml` like:

```json
[
  {
    "title": "aaaaaaaa",
    "source": "youtube",
    "url": "https://www.youtube.com/watch?v=XdTgb7r_8v0",
    "video_id": "XdTgb7r_8v0"
  },
  {
    "title": "bbbbbbbb",
    "source": "tiktok",
    "url": "https://www.tiktok.com/@lala5396628/video/7384241813214858501",
    "video_id": "7384241813214858501"
  }
]
```

Execute `etl.py` to convert videos based on the source json file to texts.

Check the `video_etl_[date]_[time].log` for converting detail.

After conversion is finished, execute `copy_text.py` to copy the converted texts to the folder specified in the `modified_output_directory` of `config.yaml`

Execute `streamlit run modify-texts-app.py` to modify texts.

Ensure everything is correct, then execute `add_texts_to_chrome.py` to insert texts into the target vectore database.
