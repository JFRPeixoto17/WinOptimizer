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
#define MyAppVersion     "1.3.3"
#define MyAppPublisher   "João Filipe Reis Peixoto"
#define MyAppExeName     "WinOptimizerPro.exe"
; Stable GUID: keeping it identical across releases lets Inno Setup
; perform an in-place upgrade instead of a side-by-side install.
#define MyAppId          "{{7E1D4B9A-3C52-4F08-A6D1-92B4E5C70F13}}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
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
; Windows 10 1809+ / Windows 11 (tweaks are audited for Win11)
MinVersion=10.0.17763
; Ask Windows to close a running instance before upgrading
CloseApplications=yes
RestartApplications=no
SetupIconFile=..\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
LicenseFile=..\LICENSE.txt
VersionInfoVersion={#MyAppVersion}
VersionInfoProductName={#MyAppName}

[Languages]
Name: "english";    MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

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
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
// ── Upgrade / downgrade detection ─────────────────────────────
function GetInstalledVersion(): String;
var
  UninstKey: String;
begin
  Result := '';
  UninstKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\' +
               ExpandConstant('{#MyAppId}') + '_is1';
  if not RegQueryStringValue(HKLM, UninstKey, 'DisplayVersion', Result) then
    RegQueryStringValue(HKCU, UninstKey, 'DisplayVersion', Result);
end;

function InitializeSetup(): Boolean;
var
  Installed: String;
  Cmp: Integer;
begin
  Result := True;
  Installed := GetInstalledVersion();
  if Installed <> '' then
  begin
    Cmp := CompareStr(Installed, '{#MyAppVersion}');
    if Cmp = 0 then
      Result := MsgBox(ExpandConstant('{#MyAppName} {#MyAppVersion} is already installed.') + #13#10 +
                'Do you want to reinstall it?', mbConfirmation, MB_YESNO) = IDYES
    else if Cmp > 0 then
      Result := MsgBox('A newer version (' + Installed + ') is already installed.' + #13#10 +
                'Continuing will DOWNGRADE to {#MyAppVersion}. Continue?',
                mbError, MB_YESNO) = IDYES
    else
      // Older version present: silent in-place upgrade (same AppId).
      Result := True;
  end;
end;

// ── Uninstall: keep or remove license/state ───────────────────
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    DataDir := ExpandConstant('{userappdata}') + '\WinOptimizer';
    if DirExists(DataDir) then
    begin
      // license.json holds the user's Pro license — never delete silently.
      if MsgBox('Remove your WinOptimizer settings and Pro license key as well?' + #13#10 +
                '(Choose No to keep them for a future reinstall.)',
                mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
        DelTree(DataDir, True, True, True);
    end;
  end;
end;
