import os
import json

class AIStudioPipeline:
    def __init__(self):
        self.root = r"C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"

    def route_request(self, task_type):
        routing_table = {
            "reasoning": "Google AI Studio Gemini 3.5-Flash / Kimi K3",
            "software_engineering": "DeepSeek V4-Pro / DeepSeek-R1 14B",
            "agentic_automation": "GLM-5.3",
            "multimodal_vision": "MiMo-V2.6-Pro",
            "math_logic": "GPT-oss 120B / MiniMax M3",
            "local_fallback": "Qwen3.6-35B-A3B / Gemma 4"
        }
        return routing_table.get(task_type, "Gemini 3.5-Flash")

if __name__ == "__main__":
    pipe = AIStudioPipeline()
    print(f"[✓] AI_Studio Pipeline Active. Primary Coding Route: {pipe.route_request('software_engineering')}")