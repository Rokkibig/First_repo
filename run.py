import asyncio
import uvicorn
from app.main import app, set_workflow
from workflows.graph_builder import build_legal_workflow
from services.llm_service import initialize_llms
from utils.metrics import setup_monitoring

async def startup():
    """Initialize all services on startup"""

    # Initialize LLMs
    print("🤖 Initializing LLMs...")
    await initialize_llms()

    # Build LangGraph workflow
    print("🔧 Building LangGraph workflow...")
    workflow = build_legal_workflow()
    set_workflow(workflow)

    # Setup monitoring
    print("📊 Setting up monitoring...")
    setup_monitoring()

    print("✅ Legal AI Agent ready!")
    return workflow

if __name__ == "__main__":
    # Run startup tasks
    asyncio.run(startup())

    # Start FastAPI server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
