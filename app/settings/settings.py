from dotenv import load_dotenv
import pathlib
import os

load_dotenv()

ROOT_DIR = pathlib.Path.cwd().parent
LOCAL_DATA_PATH = ROOT_DIR.joinpath("data")