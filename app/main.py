from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.security.input_guard import inspect_prompt
from app.llm.service import llm_service

app = FastAPI(title="AI Security Platform", description="Security gateway for LLM and agentic applications", version="0.3.0")

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10_000)
    max_new_tokens: int = Field(default=50, ge=1, le=200)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-security-platform", "version": "0.3.0"}

@app.post("/v1/prompt")
def process_prompt(request: PromptRequest):
    result = inspect_prompt(request.prompt)
    if not result["allowed"]:
        raise HTTPException(status_code=400, detail={"message": "Prompt blocked by security policy", "reason": result["reason"]})
    return {"status": "accepted", "security": result}

@app.post("/v1/generate")
def generate(request: GenerateRequest):
    security = inspect_prompt(request.prompt)
    if not security["allowed"]:
        raise HTTPException(status_code=400, detail={"message": "Prompt blocked by security policy", "reason": security["reason"]})
    generation = llm_service.generate(prompt=request.prompt, max_new_tokens=request.max_new_tokens)
    return {"status": "completed", "security": security, "generation": generation}
