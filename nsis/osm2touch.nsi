!include "MUI2.nsh"





; Osm2Touch.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects.
;
; See install-shared.nsi for a more robust way of checking for administrator rights.
; See install-per-user.nsi for a file association example.

;--------------------------------

; The name of the installer
Name "OpenStreetTouch"

; The file to write
OutFile "OpenStreetTouch_Windows_setup.exe"

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $PROGRAMFILES\OpenStreetTouch

; Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\OpenStreetTouch" "Install_Dir"

;--------------------------------
; Pages configuration
;!define MUI_HEADERIMAGE 1
;!define MUI_HEADERIMAGE_BITMAP "InstallerLogo.bmp"
;!define MUI_BRANDING
;!define MUI_BRANDING_BITMAP "InstallerLogo.bmp"
;!define MUI_HEADERIMAGE_RIGHT
!define MUI_ICON "OpenStreetTouch.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\win.bmp" ; optional
;!define MUI_ABORTWARNING


; Pages
!insertmacro MUI_PAGE_WELCOME
;!insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
;!insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
  
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"
!addplugindir ".\"

;--------------------------------

; The stuff to install
Section "OpenStreetTouch (required)"
  InitPluginsDir
  SectionIn RO
  
    ; Set output path to the installation directory.
    SetOutPath $INSTDIR
    
    ; Put file there
    File "OpenStreetTouch.exe"
    File "osm2touch_parameters.json"
    File "_internal.zip"
   
    AccessControl::GrantOnFile \
    "$INSTDIR\osm2touch_parameters.json" "(BU)" "GenericRead + GenericWrite"
    Pop $0 ; "error" on errors
  
   
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\Osm2Touch "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenStreetTouch" "DisplayName" "OpenStreetTouch"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenStreetTouch" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenStreetTouch" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenStreetTouch" "NoRepair" 1
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  RMDir /r $INSTDIR\_internal
  Pop $0
  nsisunz::UnzipToLog "$INSTDIR\_internal.zip" "$INSTDIR"
  ; Always check result on stack
  Pop $0
  StrCmp $0 "success" ok
  DetailPrint "$0" ;print error message to log
ok:
  SectionEnd


; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\OpenStreetTouch"
  CreateShortcut "$SMPROGRAMS\OpenStreetTouch\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  CreateShortcut "$SMPROGRAMS\OpenStreetTouch\OpenStreetTouch.lnk" "$INSTDIR\OpenStreetTouch.exe"

SectionEnd

Section "Desktop Shortcuts"
  SetShellVarContext current
  CreateShortCut "$DESKTOP\OpenStreetTouch.lnk" "$INSTDIR\OpenStreetTouch.exe"
  
SectionEnd



;--------------------------------
;Descriptions

  ;Language strings
  ;LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  ;!insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenStreetTouch"
  DeleteRegKey HKLM SOFTWARE\OpenStreetTouch

  ; Remove files and uninstaller
  Delete $INSTDIR\OpenStreetTouch.exe
  
  
  Delete $INSTDIR\uninstall.exe
  
  ;Delete $INSTDIR\ChromeSetup.EXE
  Delete $INSTDIR\_internal.zip
  RMDir $INSTDIR\_internal

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\OpenStreetTouch\*.lnk"
    
  ; Remove directories
  RMDir "$SMPROGRAMS\OpenStreetTouch"
  RMDir /r $INSTDIR\_internal
  RMDir "$INSTDIR"

  SetShellVarContext current
  Delete "$DESKTOP\OpenStreetTouch.lnk" 

SectionEnd
