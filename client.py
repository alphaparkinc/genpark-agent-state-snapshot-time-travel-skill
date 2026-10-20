"""Agent State Snapshot & Time-Travel Skill.
100% Python Standard Library.
"""
import json
import time
import hashlib

class AgentStateSnapshotTimeTravel:
    """Agent state snapshot and time-travel rollback engine."""

    def __init__(self):
        self.snapshots = {}
        self.timeline = []

    def save_checkpoint(self, state: dict, description: str = "") -> dict:
        state_serialized = json.dumps(state, sort_keys=True)
        state_hash = hashlib.sha256(state_serialized.encode("utf-8")).hexdigest()[:12]
        checkpoint_id = f"ckpt_{len(self.timeline) + 1}_{state_hash}"

        self.snapshots[checkpoint_id] = {
            "checkpoint_id": checkpoint_id,
            "timestamp": time.time(),
            "state": json.loads(state_serialized),
            "hash": state_hash,
            "description": description
        }
        self.timeline.append(checkpoint_id)
        return {"checkpoint_id": checkpoint_id, "hash": state_hash, "total_checkpoints": len(self.timeline)}

    def rollback(self, target_checkpoint_id: str) -> dict:
        if target_checkpoint_id not in self.snapshots:
            return {"success": False, "error": f"Checkpoint {target_checkpoint_id} not found"}

        target_idx = self.timeline.index(target_checkpoint_id)
        abandoned_ids = self.timeline[target_idx + 1:]
        self.timeline = self.timeline[:target_idx + 1]

        for aid in abandoned_ids:
            self.snapshots.pop(aid, None)

        return {
            "success": True,
            "active_checkpoint_id": target_checkpoint_id,
            "restored_state": self.snapshots[target_checkpoint_id]["state"],
            "pruned_checkpoints_count": len(abandoned_ids)
        }
