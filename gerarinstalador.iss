[Setup]
AppName=Balança API
AppVersion=1.0
DefaultDirName={pf}\BalancaAPI
DefaultGroupName=Balança API
OutputBaseFilename=instalador_balanca
Compression=lzma
SolidCompression=yes
SetupIconFile=favicon.ico
UninstallDisplayIcon={app}\balanca.exe

[Files]
Source: "dist\balanca.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "favicon.ico";    DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Balança API"; Filename: "{app}\balanca.exe"; IconFilename: "{app}\favicon.ico"; Parameters: "--settings"
Name: "{commonprograms}\Balança API"; Filename: "{app}\balanca.exe"; IconFilename: "{app}\favicon.ico"; Parameters: "--settings"
Name: "{commonstartup}\Balança API"; Filename: "{app}\balanca.exe"; WorkingDir: "{app}"; IconFilename: "{app}\favicon.ico";

[Run]
Filename: "{app}\balanca.exe"; Description: "Iniciar Balança API agora"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "taskkill"; Parameters: "/F /IM balanca.exe"; StatusMsg: "Encerrando Balança API..."; RunOnceId: "KillBalanca"
