param([string]$Action = "Toggle")
$Workspace = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"
$StateFile = Join-Path $Workspace "stack_state.json"
$LogDir    = Join-Path $Workspace "logs"
$ModelsDir = Join-Path $Workspace "models"
$CacheDir  = Join-Path $Workspace "cache\huggingface"

function Toast([string]$Title, [string]$Msg) {
    Add-Type -AssemblyName System.Windows.Forms
    $notify = New-Object System.Windows.Forms.NotifyIcon
    $notify.Icon = [System.Drawing.SystemIcons]::Information
    $notify.BalloonTipTitle = $Title
    $notify.BalloonTipText  = $Msg
    $notify.Visible         = $True
    $notify.ShowBalloonTip(3000)
    Start-Sleep -Milliseconds 500
    $notify.Dispose()
}

function Start-All {
    $env:OLLAMA_MODELS          = $ModelsDir
    $env:HF_HOME                = $CacheDir
    $env:OLLAMA_FLASH_ATTENTION = "1"
    $env:OLLAMA_KEEP_ALIVE      = "1h"

    if (-not (Get-NetTCPConnection -LocalPort 11434 -State Listen -ErrorAction SilentlyContinue)) {
        Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 2
    }

    $PyStudio = Join-Path $Workspace ".venv_studio\Scripts\python.exe"
    $StudioScript = Join-Path $Workspace "ai_studio_ipc.py"
    $pStudio = Start-Process -FilePath $PyStudio -ArgumentList "`"$StudioScript`"" -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $LogDir "studio_stdout.log") -RedirectStandardError (Join-Path $LogDir "studio_stderr.log")

    $PyTeach = Join-Path $Workspace ".venv_teach\Scripts\python.exe"
    $TeachScript = Join-Path $Workspace "teach_ipc.py"
    $pTeach = Start-Process -FilePath $PyTeach -ArgumentList "`"$TeachScript`"" -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $LogDir "teach_stdout.log") -RedirectStandardError (Join-Path $LogDir "teach_stderr.log")

    $Launcher = Join-Path $Workspace "run_webui_headless.ps1"
    $pWebUI = Start-Process powershell.exe -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Launcher`"" -WindowStyle Hidden -PassThru

    @{
        Status    = "ONLINE"
        StudioPid = $pStudio.Id
        TeachPid  = $pTeach.Id
        WebUiPid  = $pWebUI.Id
    } | ConvertTo-Json | Set-Content -Path $StateFile -Encoding utf8

    Toast "Sovereign Dev Studio" "ONLINE: All unified SSD services active."
}

function Stop-All {
    if (Test-Path $StateFile) {
        try {
            $s = Get-Content $StateFile | ConvertFrom-Json
            if ($s.StudioPid) { Stop-Process -Id $s.StudioPid -Force -ErrorAction SilentlyContinue }
            if ($s.TeachPid)  { Stop-Process -Id $s.TeachPid -Force -ErrorAction SilentlyContinue }
            if ($s.WebUiPid)  { Stop-Process -Id $s.WebUiPid -Force -ErrorAction SilentlyContinue }
        } catch {}
        Remove-Item $StateFile -Force -ErrorAction SilentlyContinue
    }

    @(3000, 9876, 9877) | ForEach-Object {
        $c = Get-NetTCPConnection -LocalPort $_ -State Listen -ErrorAction SilentlyContinue
        if ($c) { $c.OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } }
    }

    Toast "Sovereign Dev Studio" "OFFLINE: All unified services stopped."
}

$isOnline = (Test-Path $StateFile) -or (Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue)
if ($Action -eq "Toggle") { if ($isOnline) { Stop-All } else { Start-All } }
elseif ($Action -eq "Start") { Start-All }
elseif ($Action -eq "Stop")  { Stop-All }
