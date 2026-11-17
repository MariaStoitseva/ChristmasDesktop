#define MyAppName "Christmas Desktop"
#define MyAppVersion "1.0"
#define MyAppPublisher "Maria Stoitseva"
#define MyAppExeName "ChristmasDesktop.exe"

[Setup]
AppId=ChristmasDesktop.MariaStoitseva
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\ChristmasDesktop
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=ChristmasDesktopSetup

SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "dist\ChristmasDesktop\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Christmas Desktop"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\Christmas Desktop"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"
Name: "{group}\Uninstall Christmas Desktop"; Filename: "{uninstallexe}"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: none; ValueName: "ChristmasDesktop"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Christmas Desktop"; Flags: nowait postinstall skipifsilent