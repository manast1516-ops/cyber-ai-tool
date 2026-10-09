from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.orchestrator import AgentOrchestrator
from core.registry import TOOL_DEFINITIONS

app = FastAPI(
    title="Cyber AI Tool API",
    description="Local AI-powered cybersecurity analysis and diagnostic assistant.",
    version="1.0.0"
)

# Instantiate the orchestrator once on startup
agent = AgentOrchestrator()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str

@app.get("/health")
def health_check():
    return {"status": "online", "model": "llama3.2"}

@app.get("/tools")
def list_available_tools():
    return {
        name: meta["description"]
        for name, meta in TOOL_DEFINITIONS.items()
    }

@app.post("/analyze", response_model=QueryResponse)
def analyze(payload: QueryRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    result = agent.process_query(payload.query)
    return QueryResponse(query=payload.query, response=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
