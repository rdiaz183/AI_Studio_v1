param(
    [ValidateSet("Start","Stop","Status","Listen","Toggle")]
    [string]$Action = "Toggle",
    [int]$VirtualKey = 0x70 # Physical F1
)

$RootDir = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"
$DataDir = "$RootDir\Workspace\OpenWebUI_Data"
$AIStudioPort = 9876
$TeachPort = 9877
$WebUiPort = 3000

function Play-ChimeOnline {
    [Console]::Beep(523, 100)
    [Console]::Beep(659, 100)
    [Console]::Beep(784, 180)
}

function Play-ChimeOffline {
    [Console]::Beep(784, 100)
    [Console]::Beep(659, 100)
    [Console]::Beep(523, 180)
}

function Kill-PortSafe([int]$Port) {
    try {
        $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($connections) {
            $pids = $connections.OwningProcess | Select-Object -Unique
            foreach ($p in $pids) {
                if ($p -and $p -ne 0) {
                    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
                    Write-Host "[-] Closed Process $p on port :$Port" -ForegroundColor Yellow
                }
            }
        }
    } catch {}
}

function Start-SovereignStack {
    Write-Host "[+] Initializing Sovereign Native Stack..." -ForegroundColor Cyan

    # 1. Native Ollama Engine (:11434)
    if (!(Get-Process ollama -ErrorAction SilentlyContinue)) {
        Start-Process "ollama" -ArgumentList "serve" -NoNewWindow
        Start-Sleep -Seconds 2
        Write-Host "[OK] Ollama Engine Bound to :11434" -ForegroundColor Green
    }

    # 2. AI_Studio IPC (:9876) - Space-Immune Relative Execution
    Kill-PortSafe $AIStudioPort
    Start-Process "python" -ArgumentList "Bridge\aistudio_ipc_server.py" -WorkingDirectory $RootDir -NoNewWindow
    Write-Host "[OK] AI_Studio IPC Bound to :$AIStudioPort" -ForegroundColor Green

    # 3. Teach Module IPC (:9877) - Space-Immune Relative Execution
    Kill-PortSafe $TeachPort
    Start-Process "python" -ArgumentList "Bridge\teach_ipc_server.py" -WorkingDirectory $RootDir -NoNewWindow
    Write-Host "[OK] Teach IPC Bound to :$TeachPort" -ForegroundColor Green

    # 4. Native Open WebUI (:3000)
    Kill-PortSafe $WebUiPort
    $env:DATA_DIR = $DataDir
    $env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
    $env:WEBUI_AUTH = "False"

    $webuiCmd = Get-Command open-webui -ErrorAction SilentlyContinue
    if ($webuiCmd) {
        Start-Process $webuiCmd.Source -ArgumentList "serve --port $WebUiPort" -WorkingDirectory $RootDir -NoNewWindow
    } else {
        $fallback = "$env:LOCALAPPDATA\Programs\Python\Python311\Scripts\open-webui.exe"
        if (Test-Path $fallback) {
            Start-Process $fallback -ArgumentList "serve --port $WebUiPort" -WorkingDirectory $RootDir -NoNewWindow
        } else {
            Start-Process "python" -ArgumentList "-m open_webui serve --port $WebUiPort" -WorkingDirectory $RootDir -NoNewWindow
        }
    }
    Write-Host "[OK] Open WebUI Bound to :$WebUiPort" -ForegroundColor Green

    Play-ChimeOnline
    Write-Host "[ONLINE] Sovereign Stack Fully Operational on Ports 11434, 9876, 9877, 3000." -ForegroundColor Green
}

function Stop-SovereignStack {
    Write-Host "[-] Shutting Down All Sovereign Services..." -ForegroundColor Yellow
    Kill-PortSafe $WebUiPort
    Kill-PortSafe $AIStudioPort
    Kill-PortSafe $TeachPort
    Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Play-ChimeOffline
    Write-Host "[OFFLINE] All Services Stopped." -ForegroundColor Red
}

function Listen-GlobalHook {
    param([int]$Key)

    if (-not ([System.Management.Automation.PSTypeName]'Native.Keyboard').Type) {
        $Signature = '[DllImport("user32.dll")] public static extern short GetAsyncKeyState(int vKey);'
        Add-Type -MemberDefinition $Signature -Name 'Keyboard' -Namespace 'Native'
    }

    $running = [bool](Get-NetTCPConnection -LocalPort $WebUiPort -ErrorAction SilentlyContinue)
    $keyHex = "0x{0:X2}" -f $Key
    Write-Host "[*] F1 Master Hook Active (Key: $keyHex). Initial State: $(if ($running) {'ONLINE'} else {'OFFLINE'})" -ForegroundColor Cyan
    Write-Host "[*] Press F1 to toggle stack. Press [Ctrl+C] to abort listener." -ForegroundColor Gray

    while ($true) {
        if ([Native.Keyboard]::GetAsyncKeyState($Key) -band 0x8000) {
            while ([Native.Keyboard]::GetAsyncKeyState($Key) -band 0x8000) {
                Start-Sleep -Milliseconds 25
            }
            $running = -not $running
            if ($running) { Start-SovereignStack } else { Stop-SovereignStack }
        }
        Start-Sleep -Milliseconds 40
    }
}

switch ($Action) {
    "Start"  { Start-SovereignStack }
    "Stop"   { Stop-SovereignStack }
    "Listen" { Listen-GlobalHook -Key $VirtualKey }
    "Status" {
        $webui = (Get-NetTCPConnection -LocalPort $WebUiPort -ErrorAction SilentlyContinue)
        $aiActive = (Get-NetTCPConnection -LocalPort $AIStudioPort -ErrorAction SilentlyContinue)
        $teachActive = (Get-NetTCPConnection -LocalPort $TeachPort -ErrorAction SilentlyContinue)
        $ollama = (Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue)
        Write-Host "Open WebUI    (:3000)  : $(if ($webui) {'ONLINE'} else {'OFFLINE'})" -ForegroundColor $(if ($webui) {'Green'} else {'Red'})
        Write-Host "AI_Studio IPC (:9876)  : $(if ($aiActive) {'ONLINE'} else {'OFFLINE'})" -ForegroundColor $(if ($aiActive) {'Green'} else {'Red'})
        Write-Host "Teach Engine  (:9877)  : $(if ($teachActive) {'ONLINE'} else {'OFFLINE'})" -ForegroundColor $(if ($teachActive) {'Green'} else {'Red'})
        Write-Host "Ollama Engine (:11434) : $(if ($ollama) {'ONLINE'} else {'OFFLINE'})" -ForegroundColor $(if ($ollama) {'Green'} else {'Red'})
    }
    "Toggle" {
        $webui = (Get-NetTCPConnection -LocalPort $WebUiPort -ErrorAction SilentlyContinue)
        if ($webui) { Stop-SovereignStack } else { Start-SovereignStack }
    }
}