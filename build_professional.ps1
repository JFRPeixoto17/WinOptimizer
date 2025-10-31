# WinOptimizer Pro - Professional Build Script
# Creates a single-file, dependency-free Windows executable

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║          WinOptimizer Pro - Professional Build           ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}
Write-Host "✓ $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check/Install PyInstaller
Write-Host "[2/6] Checking PyInstaller..." -ForegroundColor Yellow
pip show pyinstaller > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}
Write-Host "✓ PyInstaller ready" -ForegroundColor Green
Write-Host ""

# Check/Install UPX (optional compression)
Write-Host "[3/6] Checking UPX compressor..." -ForegroundColor Yellow
$upxPath = Get-Command upx -ErrorAction SilentlyContinue
if ($null -eq $upxPath) {
    Write-Host "  ⚠️  UPX not found (optional - reduces .exe size by 30-40%)" -ForegroundColor Yellow
    Write-Host "  Download from: https://github.com/upx/upx/releases" -ForegroundColor Gray
    Write-Host "  Continuing without compression..." -ForegroundColor Yellow
} else {
    Write-Host "✓ UPX available for compression" -ForegroundColor Green
}
Write-Host ""

# Create icon placeholder if missing
Write-Host "[4/6] Checking application icon..." -ForegroundColor Yellow
if (-not (Test-Path "icon.ico")) {
    Write-Host "  ⚠️  icon.ico not found - build will use default icon" -ForegroundColor Yellow
    Write-Host "  Create icon.ico (256x256) for custom branding" -ForegroundColor Gray
} else {
    Write-Host "✓ Custom icon found" -ForegroundColor Green
}
Write-Host ""

# Clean previous builds
Write-Host "[5/6] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
Write-Host "✓ Build directories cleaned" -ForegroundColor Green
Write-Host ""

# Build executable
Write-Host "[6/6] Building WinOptimizerPro.exe..." -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Check if spec file exists
if (Test-Path "WinOptimizerPro.spec") {
    # Use spec file for full control
    python -m PyInstaller --clean --noconfirm WinOptimizerPro.spec
} else {
    # Fallback to command-line build
    python -m PyInstaller --onefile `
        --windowed `
        --name="WinOptimizerPro" `
        --add-data "tweaks.json;." `
        --icon=icon.ico `
        --clean `
        --noconfirm `
        --uac-admin `
        main.py
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Check build success
if (Test-Path "dist\WinOptimizerPro.exe") {
    $exeSize = (Get-Item "dist\WinOptimizerPro.exe").Length / 1MB
    
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                          ║" -ForegroundColor Green
    Write-Host "║                 ✓ BUILD SUCCESSFUL!                      ║" -ForegroundColor Green
    Write-Host "║                                                          ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Executable created:" -ForegroundColor Cyan
    Write-Host "   Location: dist\WinOptimizerPro.exe" -ForegroundColor White
    Write-Host "   Size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ FEATURES:" -ForegroundColor Cyan
    Write-Host "   • Standalone executable (no dependencies needed)" -ForegroundColor White
    Write-Host "   • Works on fresh Windows 10/11 installations" -ForegroundColor White
    Write-Host "   • No console window (pure GUI)" -ForegroundColor White
    Write-Host "   • Auto-requests admin privileges (UAC prompt)" -ForegroundColor White
    Write-Host "   • Custom icon and version info" -ForegroundColor White
    Write-Host "   • Silent PowerShell execution" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 TO DISTRIBUTE:" -ForegroundColor Cyan
    Write-Host "   1. Copy dist\WinOptimizerPro.exe to target PC" -ForegroundColor White
    Write-Host "   2. Double-click to run (UAC prompt will appear)" -ForegroundColor White
    Write-Host "   3. No installation or dependencies required!" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 OPTIONAL IMPROVEMENTS:" -ForegroundColor Yellow
    Write-Host "   • Add icon.ico (256x256) for custom branding" -ForegroundColor Gray
    Write-Host "   • Install UPX to reduce file size by 30-40%" -ForegroundColor Gray
    Write-Host "   • Create installer with Inno Setup or NSIS" -ForegroundColor Gray
    Write-Host ""
    
    # Test the executable
    Write-Host "🔍 Would you like to test the executable now? (y/n): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host ""
        Write-Host "Launching WinOptimizerPro.exe..." -ForegroundColor Yellow
        Start-Process "dist\WinOptimizerPro.exe"
    }
    
} else {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║                                                          ║" -ForegroundColor Red
    Write-Host "║                   ✗ BUILD FAILED!                        ║" -ForegroundColor Red
    Write-Host "║                                                          ║" -ForegroundColor Red
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above for details." -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
