from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_llm(**kwargs):
    """
    Return a language model instance (to be implemented later).
    """
    raise NotImplementedError("get_llm() not implemented yet.")

