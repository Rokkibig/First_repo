from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.auth import verify_token
from services.audit_service import audit_log

app = FastAPI(
    title="Legal AI Agent API",
    description="Data-driven legal practice AI system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

legal_workflow = None

def set_workflow(workflow):
    global legal_workflow
    legal_workflow = workflow

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "legal-ai-agent"}

@app.post("/api/v1/process")
async def process_request(request: dict, current_user=Depends(verify_token)):
    await audit_log(user=current_user, action="process_request", details=request)
    if legal_workflow is None:
        return {"error": "Workflow not initialized"}
    result = await legal_workflow.ainvoke(request)
    return result
