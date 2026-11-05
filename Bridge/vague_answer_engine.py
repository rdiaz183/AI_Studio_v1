import sys, json

def evaluate_clarity(prompt):
    words = prompt.split()
    if len(words) < 15:
        return {
            "status": "VAGUE_PROMPT_DETECTED",
            "tier": 1,
            "clarifications": [
                "1. Target subsystem: Unreal Engine 5.5 (Chaos/C++20), Blender 5.2 (Python API), or Godot 4.x?",
                "2. Specific memory constraints and physics tick groups (TG_PrePhysics, TG_DuringPhysics)?",
                "3. Inter-process socket packet schema or binary length prefix parameters?"
            ]
        }
    return {"status": "READY_FOR_EXECUTION", "tier": 4}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(evaluate_clarity(query)))
