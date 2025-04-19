[Setup]
AppName=AI Translator
AppVersion=1.1.2
DefaultDirName={pf}\AITranslator
DefaultGroupName=AITranslator
OutputBaseFilename=AITranslator_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\AITranslator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\AI Translator"; Filename: "{app}\AITranslator.exe"
Name: "{group}\Uninstall AI Translator"; Filename: "{uninstallexe}"
Name: "{group}\AI Translator"; Filename: "{app}\AITranslator.exe"; IconFilename: "{app}\icon.ico"
