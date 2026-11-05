# Sovereign Git Synchronization Bridge
$Workspace = "C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace"
Set-Location $Workspace

if (-not (Test-Path (Join-Path $Workspace ".git"))) {
    git init
    git remote add origin "https://github.com/rdiaz183/AI_Studio_v1.git"
}

git add -A
$status = git status --porcelain
if ($status) {
    $commitMsg = "chore(sync): automated workspace synchronization $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m "$commitMsg"
    Write-Host "[✓] Git Commit Created: $commitMsg" -ForegroundColor Green
    try {
        git push origin main
        Write-Host "[✓] Successfully synchronized with GitHub remote." -ForegroundColor Green
    } catch {
        Write-Warning "[!] Remote push deferred. Verify network and remote credentials."
    }
} else {
    Write-Host "[✓] Workspace clean. No pending changes to commit." -ForegroundColor Green
}
