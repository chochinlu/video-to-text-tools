import os
import shutil
import yaml

try:
    # Read config.yaml configuration file
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    source_dir = config["output_directory"]
    target_dir = config["modified_output_directory"]

    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Copy all contents from source_dir to target_dir
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        target_item = os.path.join(target_dir, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, target_item, dirs_exist_ok=True)
        else:
            shutil.copy2(source_item, target_item)

    print(f"All contents have been copied from {source_dir} to {target_dir}")

except FileNotFoundError as e:
    print(f"File not found: {e}")
except PermissionError as e:
    print(f"Permission error: {e}")
except yaml.YAMLError as e:
    print(f"Error reading YAML file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
