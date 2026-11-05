$env:DATA_DIR         = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace\open-webui-data"
$env:OLLAMA_MODELS    = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace\models"
$env:HF_HOME          = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace\cache\huggingface"
$env:OLLAMA_BASE_URL  = "http://127.0.0.1:11434"
$env:WEBUI_SECRET_KEY = "sovereign-ai-studio-secret-key-2026"
$env:WEBUI_AUTH       = "true"
Set-Location "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"
& "C:\Users\rdiaz\AppData\Local\Programs\Python\Python311\Scripts\open-webui.exe" serve --port 3000
