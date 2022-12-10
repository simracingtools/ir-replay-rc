; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

; Change this base path to your needs
#define ProjectBaseDir "."

#define MyAppName "irRC"
#define MyAppVersion "1.1"
#define MyAppPublisher "Bausdorf engineering"
#define MyAppURL "https://github.com/robbyb67/simracing/tree/master/ir-replay-rc"
#define MyAppExeName "irRcApp.exe"

[Setup]
SourceDir={#ProjectBaseDir}
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId=783D5417-7A0A-417F-893D-80F8C0187817
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DefaultUserInfoName=
DefaultUserInfoOrg=
;UsePreviousUserInfo=yes
AllowNoIcons=yes
LicenseFile={#ProjectBaseDir}\LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputDir={#ProjectBaseDir}\dist
OutputBaseFilename=irrcSetup
Compression=lzma
SolidCompression=yes
SetupIconFile={#ProjectBaseDir}\dist\tesseract-colored.ico
;UserInfoPage=yes
WizardStyle=modern
WizardImageFile=bausdorfengineering.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Messages]
UserInfoName=&iRacing ID:
UserInfoOrg=&Client access token:

[INI]
;Filename: "{app}\irrc.ini"; Section: "global"; Key: "iracingId"; String: "{userinfoname}"
;Filename: "{app}\irrc.ini"; Section: "connect"; Key: "clientAccessToken"; String: "{userinfoorg}"
Filename: "{app}\irrc.ini"; Section: "connect"; Key: "postUrl"; String: "https://race-control.bausdorf-engineering.de/clientmessage"
Filename: "{app}\irrc.ini"; Section: "connect"; Key: "wsUrl"; String: "wss://race-control.bausdorf-engineering.de/rcclient"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#ProjectBaseDir}\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectBaseDir}\dist\tesseract-colored.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectBaseDir}\dist\tesseract-irrc.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectBaseDir}\dist\irrc.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectBaseDir}\dist\liesmich.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectBaseDir}\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\tesseract-irrc.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\tesseract-irrc.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch application"; Flags: postinstall nowait skipifsilent
