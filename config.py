import os

DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)