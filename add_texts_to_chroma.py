import os
import yaml
from dotenv import load_dotenv
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Read the modified texts
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
    file_path = config["modified_output_directory"]


# Create persistent client
client = chromadb.PersistentClient(path=config["chromadb"]["path"])

# Set embedding model
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),  # Read API key from environment variable
    model_name=config["chromadb"]["embedding_model"],
)

# get or create a collection
collection = client.get_or_create_collection(
    name=config["chromadb"]["collection_name"],
    embedding_function=openai_ef,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config["text_splitter"]["chunk_size"],
    chunk_overlap=config["text_splitter"]["overlap_size"],
)

for file_name in os.listdir(file_path):
    if file_name.endswith(".txt"):
        with open(os.path.join(file_path, file_name), "r") as file:
            # file name用第一個_分割, 分割後的第一個元素叫做source,
            # 第二個元素叫做video_id, 是扣掉第一個元素後剩下的部分
            source, video_id = file_name.split("_", 1)

            # split the text
            texts = text_splitter.split_text(file.read())

            # create a metadata
            metadata = {
                "source": source,
                "video_id": video_id,
            }

            # create a metadata array with the same length as the text.
            metadatas = [metadata] * len(texts)

            # insert the texts and metadatas into the collection
            collection.add(
                ids=[f"{source}_{video_id}_{i}" for i in range(len(texts))],
                documents=texts,
                metadatas=metadatas,
            )
