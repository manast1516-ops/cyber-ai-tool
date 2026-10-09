from langchain_ollama import OllamaLLM

def get_llm(model_name: str = "llama3.2", base_url: str = "http://localhost:11434", temperature: float = 0.2):
    """
    Initializes and returns a local Ollama LLM instance using langchain-ollama.
    """
    llm = OllamaLLM(
        base_url=base_url,
        model=model_name,
        temperature=temperature
    )
    return llm
