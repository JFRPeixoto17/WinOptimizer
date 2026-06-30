; ──────────────────────────────────────────────────────────────
;  WinOptimizer Pro - Inno Setup Installer Script
;  Build with: iscc installer\WinOptimizer.iss   (Inno Setup 6+)
;  Produces:   installer\Output\WinOptimizerPro-Setup.exe
;
;  Prerequisite: build the EXE first with build_professional.ps1
;  so that dist\WinOptimizerPro.exe exists.
;
;  Author: João Filipe Reis Peixoto
;  Copyright (c) 2025 João Filipe Reis Peixoto. All rights reserved.
; ──────────────────────────────────────────────────────────────

#define MyAppName        "WinOptimizer Pro"
#define MyAppVersion     "1.3.0"
#define MyAppPublisher   "João Filipe Reis Peixoto"
#define MyAppExeName     "WinOptimizerPro.exe"
#define MyAppId          "{{8F3A2C1D-6B4E-4A9F-9E2D-WINOPT130PRO}}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\WinOptimizer Pro
DefaultGroupName=WinOptimizer Pro
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=WinOptimizerPro-Setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
; The app modifies system settings, so it must run elevated.
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=..\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=..\LICENSE.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
; Built executable (run build_professional.ps1 first)
Source: "..\dist\WinOptimizerPro.exe"; DestDir: "{app}"; Flags: ignoreversion
; Ship docs alongside
Source: "..\README.md";   DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\WinOptimizer Pro"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall WinOptimizer Pro"; Filename: "{uninstallexe}"
Name: "{autodesktop}\WinOptimizer Pro"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Offer to launch after install (elevated, since PrivilegesRequired=admin)
Filename: "{app}\{#MyAppExeName}"; Description: "Launch WinOptimizer Pro"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove per-user config/state/license written by the app
Type: filesandordirs; Name: "{userappdata}\WinOptimizer"
