"""
title: AI_Studio Sovereign Toolset
author: AI_Studio v1
version: 1.0.0
description: Direct bridge to AI_Studio IPC (:9876), Teach Engine (:9877), and local AST gates.
"""

import requests
import json
import subprocess
import os

class Tools:
    def __init__(self):
        self.ai_studio_url = "http://127.0.0.1:9876"
        self.teach_url = "http://127.0.0.1:9877"
        self.workspace = r"C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"

    def audit_toolchain(self) -> str:
        """
        Check the status of Visual Studio, Unreal Engine 5.8, Blender 5.2, and Godot.
        :return: JSON formatted toolchain audit.
        """
        audit_file = os.path.join(self.workspace, "Workspace", "Logs", "toolchain_audit.json")
        if os.path.exists(audit_file):
            with open(audit_file, "r", encoding="utf-8") as f:
                return f.read()
        return "Toolchain audit log not found. Run software_update_checker.py"

    def verify_ast_syntax(self, relative_path: str = "Bridge/aistudio_ipc_server.py") -> str:
        """
        Verify Python or C++ structures for syntax safety before committing to disk.
        :param relative_path: Relative path to the target file.
        :return: AST compiler audit output.
        """
        target = os.path.join(self.workspace, relative_path)
        simulator = os.path.join(self.workspace, "Bridge", "test_simulator.py")
        res = subprocess.run(["python", simulator, target], capture_output=True, text=True)
        return res.stdout if res.stdout else res.stderr

    def query_teach_engine(self, curriculum_track: str, concept_query: str) -> str:
        """
        Submit a technical question to the Teach Engine on Port 9877 for C++ mentorship.
        :param curriculum_track: Topic area (e.g. 'Unreal C++', 'Chaos Substepping').
        :param concept_query: Specific question or code snippet.
        :return: Mentorship response from Teach IPC.
        """
        try:
            res = requests.post(self.teach_url, json={"track": curriculum_track, "query": concept_query}, timeout=5)
            return json.dumps(res.json(), indent=2)
        except Exception as e:
            return f"Teach Engine unreachable: {e}"