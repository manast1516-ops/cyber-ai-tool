import os
from dotenv import load_dotenv

load_dotenv()

# LLM / Ollama Endpoint Configuration
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3.2")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Vector Store / RAG Configuration
CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")

# Network Interface Settings
DEFAULT_INTERFACE: str = os.getenv("DEFAULT_INTERFACE", "wlan0")
PACKET_CAPTURE_COUNT: int = int(os.getenv("PACKET_CAPTURE_COUNT", "50"))
