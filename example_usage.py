"""Example usage for Agent State Snapshot & Time-Travel Skill."""
from client import AgentStateSnapshotTimeTravel
import json

tt = AgentStateSnapshotTimeTravel()

# 1. Save state after planning
c1 = tt.save_checkpoint({"step": 1, "plan": ["Search database", "Draft report"]}, "Initial planning complete")
print("Saved C1:", json.dumps(c1))

# 2. Save state after query execution
c2 = tt.save_checkpoint({"step": 2, "plan": ["Draft report"], "data": [1, 2, 3]}, "Data retrieved")
print("Saved C2:", json.dumps(c2))

# 3. Simulate failure in step 3, rollback to C1
res = tt.rollback(c1["checkpoint_id"])
print("Rollback result:", json.dumps(res, indent=2))
