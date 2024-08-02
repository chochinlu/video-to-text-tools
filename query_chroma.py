import yaml
from dotenv import load_dotenv
import chromadb

load_dotenv()

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

client = chromadb.PersistentClient(path=config["chromadb"]["path"])

print(client.list_collections())

collection = client.get_collection(config["chromadb"]["collection_name"])

print(collection.count())

print(collection.get([]))
