
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_FILE = BASE_DIR / "knowledge.txt"
