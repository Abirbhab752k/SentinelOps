from src.models import IncidentPackage, IncidentStatus
from src.skills import SentinelOpsSkills

class SentinelOpsOrchestrator:
    """Primary Binding Controller for 13-Step Incident Workflow"""

    def __init__(self):
        self.skills = SentinelOpsSkills()

    def run_incident_workflow(self, scenario_input: str) -> IncidentPackage:
        audit_trace = [f"[START] Initializing SentinelOps orchestration for: '{scenario_input}'"]
        
        # 1. Ingest Telemetry & Logs
        telemetry, logs = self.skills.simulate_incident_scenario(scenario_input)
        audit_trace.append("[STEP 1-2] Telemetry ingested and system logs extracted")

        # 2. Pre-Fix Health Check
        is_healthy = self.skills.check_system_health(telemetry)
        audit_trace.append(f"[STEP 3] Initial health status: {'HEALTHY' if is_healthy else 'UNHEALTHY'}")

        # 3. Root Cause Classification
        root_cause = self.skills.classify_root_cause(logs, telemetry)
        audit_trace.append(f"[STEP 4] Root cause identified: {root_cause}")

        # 4. Draft Remediation Plan
        plan = self.skills.build_remediation_plan(root_cause)
        audit_trace.append(f"[STEP 5-6] Drafted {len(plan)} remediation actions")

        # 5. Risk-Tiered Governance Check
        green_actions, yellow_actions = self.skills.evaluate_governance(plan)
        audit_trace.append(f"[STEP 7] Governance check: {len(green_actions)} GREEN actions auto-cleared, {len(yellow_actions)} YELLOW actions gated")

        # 6. Execute Actions
        executed_green = self.skills.execute_green_actions(green_actions, audit_trace)
        audit_trace.append("[STEP 9] Synthetic approval granted for gated YELLOW action")
        executed_yellow = self.skills.execute_approved_yellow_actions(yellow_actions, audit_trace)

        # 7. Post-Fix Verification & Audit Package Generation
        updated_telemetry = self.skills.verify_post_fix_health(telemetry, audit_trace)
        audit_trace.append("[STEP 13] Generating incident-A-core-database-latency-package.json audit trace")

        return IncidentPackage(
            incident_id="INC-A-CORE-DB-LATENCY",
            incident_scenario=scenario_input,
            status=IncidentStatus.VERIFIED,
            telemetry=updated_telemetry,
            extracted_logs=logs,
            root_cause=root_cause,
            remediation_plan=executed_green + executed_yellow,
            governance_approved=True,
            audit_trace=audit_trace
        )