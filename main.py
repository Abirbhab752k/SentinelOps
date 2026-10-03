from fastapi import FastAPI
from src.orchestrator import SentinelOpsOrchestrator
from src.models import IncidentPackage

app = FastAPI(
    title="SentinelOps AI Agent",
    description="Autonomous Infrastructure Triage & Incident Remediation Agent API",
    version="1.0.0"
)

orchestrator = SentinelOpsOrchestrator()

@app.get("/")
def root():
    return {"status": "Live", "agent": "SentinelOps"}

@app.post("/run", response_model=IncidentPackage)
def run_agent(prompt: str = "Simulate incident A and run diagnosis"):
    return orchestrator.run_incident_workflow(prompt)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)