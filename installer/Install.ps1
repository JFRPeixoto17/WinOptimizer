# WinOptimizer Pro - Simple Installer (NO INNO SETUP REQUIRED!)
# This script creates an installer that works with native Windows PowerShell

param(
    [switch]$CreateDesktopShortcut = $false
)

$ErrorActionPreference = "Stop"

Write-Host "`n╔══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                          ║" -ForegroundColor Cyan
Write-Host "║                  WinOptimizer Pro - Installer                            ║" -ForegroundColor Cyan
Write-Host "║                                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This installer requires administrator privileges!`n" -ForegroundColor Yellow
    Write-Host "Starting as administrator..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Check if .exe exists
$exePath = Join-Path $PSScriptRoot "..\dist\WinOptimizerPro.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "❌ ERROR: WinOptimizerPro.exe not found!" -ForegroundColor Red
    Write-Host "   Expected location: $exePath`n" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📦 Installing WinOptimizer Pro..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Installation folder
$installPath = "$env:ProgramFiles\WinOptimizer Pro"

# Create installation folder
Write-Host "📁 Creating installation folder..." -ForegroundColor Cyan
if (-not (Test-Path $installPath)) {
    New-Item -ItemType Directory -Path $installPath -Force | Out-Null
}

# Copy executable
Write-Host "📋 Copying files..." -ForegroundColor Cyan
Copy-Item $exePath -Destination $installPath -Force

# Copy documentation if exists
$readmePath = Join-Path $PSScriptRoot "..\README.md"
$licensePath = Join-Path $PSScriptRoot "..\LICENSE.txt"
if (Test-Path $readmePath) { Copy-Item $readmePath -Destination $installPath -Force }
if (Test-Path $licensePath) { Copy-Item $licensePath -Destination $installPath -Force }

# Create Start Menu shortcut
Write-Host "📌 Creating Start Menu shortcut..." -ForegroundColor Cyan
$startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut("$startMenuPath\WinOptimizer Pro.lnk")
$shortcut.TargetPath = "$installPath\WinOptimizerPro.exe"
$shortcut.WorkingDirectory = $installPath
$shortcut.Description = "Professional Windows Performance Optimizer"
$shortcut.Save()

# Ask about desktop shortcut
Write-Host "`n❓ Do you want to create a desktop shortcut? (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host
if ($response -eq "Y" -or $response -eq "y" -or $response -eq "Yes" -or $response -eq "yes") {
    Write-Host "📌 Creating desktop shortcut..." -ForegroundColor Cyan
    $desktopPath = [Environment]::GetFolderPath("CommonDesktopDirectory")
    $desktopShortcut = $WScriptShell.CreateShortcut("$desktopPath\WinOptimizer Pro.lnk")
    $desktopShortcut.TargetPath = "$installPath\WinOptimizerPro.exe"
    $desktopShortcut.WorkingDirectory = $installPath
    $desktopShortcut.Description = "Professional Windows Performance Optimizer"
    $desktopShortcut.Save()
}

# Create uninstaller
Write-Host "🗑️  Creating uninstaller..." -ForegroundColor Cyan
$uninstallScript = @"
# WinOptimizer Pro - Uninstaller

`$installPath = "$installPath"
`$startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\WinOptimizer Pro.lnk"
`$desktopPath = "[Environment]::GetFolderPath("CommonDesktopDirectory")\WinOptimizer Pro.lnk"

Write-Host "Uninstalling WinOptimizer Pro..." -ForegroundColor Yellow

# Remove shortcuts
if (Test-Path `$startMenuPath) { Remove-Item `$startMenuPath -Force }
if (Test-Path `$desktopPath) { Remove-Item `$desktopPath -Force }

# Remove installation folder
if (Test-Path `$installPath) { 
    Remove-Item `$installPath -Recurse -Force 
    Write-Host "✓ WinOptimizer Pro uninstalled successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installation folder not found." -ForegroundColor Yellow
}

Write-Host "Press Enter to exit..."
Read-Host
"@

$uninstallScript | Out-File -FilePath "$installPath\Uninstall.ps1" -Encoding UTF8

# Create uninstaller shortcut in Start Menu
$uninstallShortcut = $WScriptShell.CreateShortcut("$startMenuPath\Uninstall WinOptimizer Pro.lnk")
$uninstallShortcut.TargetPath = "powershell.exe"
$uninstallShortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$installPath\Uninstall.ps1`""
$uninstallShortcut.Description = "Uninstall WinOptimizer Pro"
$uninstallShortcut.Save()

Write-Host "`n╔══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                                          ║" -ForegroundColor Green
Write-Host "║                 ✓ INSTALLATION COMPLETED SUCCESSFULLY!                   ║" -ForegroundColor Green
Write-Host "║                                                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📍 Installation location:" -ForegroundColor Cyan
Write-Host "   $installPath`n" -ForegroundColor White

Write-Host "🚀 How to use:" -ForegroundColor Yellow
Write-Host "   • Start Menu → Search 'WinOptimizer Pro'" -ForegroundColor White
Write-Host "   • Desktop shortcut (if created)" -ForegroundColor White
Write-Host "   • Direct file: $installPath\WinOptimizerPro.exe`n" -ForegroundColor White

Write-Host "🗑️  To uninstall:" -ForegroundColor Yellow
Write-Host "   Start Menu → 'Uninstall WinOptimizer Pro'`n" -ForegroundColor White

Write-Host "Press Enter to exit..."
Read-Host
