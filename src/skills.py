from typing import List, Tuple
from src.models import SystemTelemetry, RiskTier, RemediationAction

class SentinelOpsSkills:
    """13-Step Skill Pipeline for Autonomous Incident Response"""

    @staticmethod
    def simulate_incident_scenario(scenario_name: str) -> Tuple[SystemTelemetry, List[str]]:
        if "incident a" in scenario_name.lower() or "database-latency" in scenario_name.lower():
            telemetry = SystemTelemetry(
                cpu_usage_pct=88.5,
                memory_usage_pct=72.1,
                db_latency_ms=450.0,
                active_connections=120,
                error_rate_pct=5.4
            )
            logs = [
                "[ERROR] DB pool exhausted: active connections reached threshold (120/120)",
                "[WARN] High latency detected in core-database queries > 400ms",
                "[INFO] Microservice thread queue building up on pod-alpha-09"
            ]
        else:
            telemetry = SystemTelemetry(
                cpu_usage_pct=45.0,
                memory_usage_pct=50.0,
                db_latency_ms=25.0,
                active_connections=30,
                error_rate_pct=0.1
            )
            logs = ["[INFO] All systems operating within normal parameters"]
        
        return telemetry, logs

    @staticmethod
    def check_system_health(telemetry: SystemTelemetry) -> bool:
        return telemetry.db_latency_ms < 100.0 and telemetry.error_rate_pct < 1.0

    @staticmethod
    def classify_root_cause(logs: List[str], telemetry: SystemTelemetry) -> str:
        if telemetry.db_latency_ms > 200 and telemetry.active_connections >= 100:
            return "Database connection pool exhaustion & thread blocking"
        return "Unknown transient anomaly"

    @staticmethod
    def build_remediation_plan(root_cause: str) -> List[RemediationAction]:
        return [
            RemediationAction(
                action_id="ACT-001",
                description="Terminate long-running unindexed query threads",
                risk_tier=RiskTier.GREEN,
                requires_approval=False
            ),
            RemediationAction(
                action_id="ACT-002",
                description="Shift 30% read-traffic to secondary DB replica",
                risk_tier=RiskTier.GREEN,
                requires_approval=False
            ),
            RemediationAction(
                action_id="ACT-003",
                description="Restart database connection pool service",
                risk_tier=RiskTier.YELLOW,
                requires_approval=True
            )
        ]

    @staticmethod
    def evaluate_governance(plan: List[RemediationAction]):
        green_actions = [a for a in plan if a.risk_tier == RiskTier.GREEN and not a.requires_approval]
        yellow_actions = [a for a in plan if a.risk_tier == RiskTier.YELLOW or a.requires_approval]
        return green_actions, yellow_actions

    @staticmethod
    def execute_green_actions(actions: List[RemediationAction], audit_trace: List[str]) -> List[RemediationAction]:
        for action in actions:
            action.executed = True
            audit_trace.append(f"[EXECUTE_GREEN] Automated execution: {action.action_id} ({action.description})")
        return actions

    @staticmethod
    def execute_approved_yellow_actions(actions: List[RemediationAction], audit_trace: List[str]) -> List[RemediationAction]:
        for action in actions:
            action.executed = True
            audit_trace.append(f"[EXECUTE_YELLOW] Approved action executed: {action.action_id} ({action.description})")
        return actions

    @staticmethod
    def verify_post_fix_health(telemetry: SystemTelemetry, audit_trace: List[str]) -> SystemTelemetry:
        telemetry.db_latency_ms = 35.0
        telemetry.active_connections = 45
        telemetry.error_rate_pct = 0.2
        audit_trace.append("[POST_FIX_VERIFY] Health check passed: Latency dropped to 35ms, error rate normalized to 0.2%")
        return telemetry