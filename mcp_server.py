"""MCP Server for Agent State Snapshot & Time-Travel Skill.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import AgentStateSnapshotTimeTravel

tt = AgentStateSnapshotTimeTravel()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "save_checkpoint",
                                "description": "Save current agent state snapshot and get checkpoint ID",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "state": {"type": "object", "description": "Agent state dictionary"},
                                        "description": {"type": "string", "default": ""}
                                    },
                                    "required": ["state"]
                                }
                            },
                            {
                                "name": "rollback",
                                "description": "Rollback agent state to a prior checkpoint and prune subsequent branches",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "checkpoint_id": {"type": "string", "description": "Target checkpoint ID"}
                                    },
                                    "required": ["checkpoint_id"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "save_checkpoint":
                    res = tt.save_checkpoint(args.get("state", {}), args.get("description", ""))
                elif call_name == "rollback":
                    res = tt.rollback(args.get("checkpoint_id", ""))
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
