import os
import streamlit as st

# 設定目錄
directory = "modified_texts"

# 讀取目錄中的所有檔案
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# 建立一個字典來儲存檔案內容
file_contents = {}

# 讀取每個檔案的內容
for file_name in files:
    with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
        file_contents[file_name] = file.read()

# 建立 Streamlit 表單
st.title("Modified Texts Editor")

# 建立一個字典來儲存修改後的內容
modified_contents = {}

# 顯示每個檔案的內容在一個獨立的 textarea 中
for file_name, content in file_contents.items():
    modified_contents[file_name] = st.text_area(
        f"Content of {file_name}", content, height=200
    )

# 當按下 submit 按鈕時，儲存修改後的內容
if st.button("Submit"):
    for file_name, content in modified_contents.items():
        with open(os.path.join(directory, file_name), "w", encoding="utf-8") as file:
            file.write(content)
    st.success("All files have been updated successfully!")
