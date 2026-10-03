from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RiskTier(str, Enum):
    GREEN = "GREEN"      # Low-risk, fully automated execution
    YELLOW = "YELLOW"    # Medium-risk, requires approval gate
    RED = "RED"          # High-risk, manual escalation

class IncidentStatus(str, Enum):
    SIMULATED = "SIMULATED"
    DIAGNOSED = "DIAGNOSED"
    GOVERNANCE_CHECKED = "GOVERNANCE_CHECKED"
    REMEDIATED = "REMEDIATED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"

class SystemTelemetry(BaseModel):
    cpu_usage_pct: float
    memory_usage_pct: float
    db_latency_ms: float
    active_connections: int
    error_rate_pct: float

class RemediationAction(BaseModel):
    action_id: str
    description: str
    risk_tier: RiskTier
    requires_approval: bool
    executed: bool = False

class IncidentPackage(BaseModel):
    incident_id: str
    incident_scenario: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    status: IncidentStatus
    telemetry: SystemTelemetry
    extracted_logs: List[str]
    root_cause: str
    remediation_plan: List[RemediationAction]
    governance_approved: bool
    audit_trace: List[str]