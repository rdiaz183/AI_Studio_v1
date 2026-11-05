# AI_Studio v1 - Sovereign Zero-Docker AI Development Platform

## Endpoints & Port Map
- AI_Studio IPC: `http://localhost:9876`
- Teach IPC: `http://localhost:9877`
- Ollama Local Engine: `http://localhost:11434`

## Quick Commands
- Hardware F1 Background Hook: `powershell -ExecutionPolicy Bypass .\F1-Daemon.ps1 -Action Listen`
- Manual Stack Toggle: `powershell -ExecutionPolicy Bypass .\F1-Daemon.ps1 -Action Toggle`
- DCC & Engine Update Audit: `python .\Bridge\software_update_checker.py`
- Run AST Compiler Test: `python .\Bridge\test_simulator.py <target_file>`