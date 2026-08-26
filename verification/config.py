import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from verification folder or project root
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent / ".env")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Models
GROQ_JUDGE_MODEL = os.getenv("GROQ_JUDGE_MODEL", "qwen/qwen3.8-27b")
GROQ_SIMULATOR_MODEL = os.getenv("GROQ_SIMULATOR_MODEL", "allam-2-7b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

# Verification parameters
PASS_THRESHOLD = int(os.getenv("PASS_THRESHOLD", "3"))  # score >= 3 -> PASS, < 3 -> FAIL
TRUTHFULQA_SUBSET_SIZE = int(os.getenv("TRUTHFULQA_SUBSET_SIZE", "60"))

# Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = PROJECT_ROOT / "docs" / "results"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
