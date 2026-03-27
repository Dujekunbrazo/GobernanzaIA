@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "PING_PONG_SCRIPT=%SCRIPT_DIR%governance_ping_pong.py"

if "%~1"=="" (
    set "TARGET_REPO=%CD%"
) else (
    set "TARGET_REPO=%~f1"
)

if not exist "%PING_PONG_SCRIPT%" (
    echo [ERROR] No encuentro el script can^onico: "%PING_PONG_SCRIPT%"
    pause
    exit /b 1
)

if not exist "%TARGET_REPO%\dev\records\initiatives" (
    echo [ERROR] El repo destino no parece tener gobernanza instalada:
    echo         "%TARGET_REPO%"
    echo.
    echo Debe existir: dev\records\initiatives
    pause
    exit /b 1
)

call :ensure_claude || exit /b 1
call :ensure_codex || exit /b 1

:menu
cls
echo ============================================================
echo Governance Ping-Pong Launcher
echo ============================================================
echo Repo destino:
echo   %TARGET_REPO%
echo.
call :print_initiatives
echo.
echo 1. Listar iniciativas
echo 2. Status de una iniciativa
echo 3. Avanzar iniciativa
echo 4. Avanzar iniciativa ^(dry-run^)
echo 5. Aprobar F2
echo 6. Crear iniciativa nueva
echo 7. Comprobar herramientas
echo 8. Salir
echo.
choice /c 12345678 /n /m "Selecciona una opcion: "

if errorlevel 8 exit /b 0
if errorlevel 7 goto tools
if errorlevel 6 goto init_new
if errorlevel 5 goto approve_f2
if errorlevel 4 goto advance_dry
if errorlevel 3 goto advance_real
if errorlevel 2 goto status_cmd
if errorlevel 1 goto list_only

:list_only
cls
echo Iniciativas en "%TARGET_REPO%\dev\records\initiatives"
echo.
call :print_initiatives
echo.
pause
goto menu

:status_cmd
call :prompt_initiative
if not defined INITIATIVE_ID goto menu
python "%PING_PONG_SCRIPT%" --target-repo "%TARGET_REPO%" status --initiative-id "%INITIATIVE_ID%"
echo.
pause
goto menu

:advance_real
call :prompt_initiative
if not defined INITIATIVE_ID goto menu
set "DIRTY_FLAG="
choice /c SN /n /m "Permitir worktree sucio con excepcion operativa si aplica? [S/N]: "
if errorlevel 2 goto advance_real_run
if errorlevel 1 set "DIRTY_FLAG=--allow-dirty-with-ask-exception"
:advance_real_run
python "%PING_PONG_SCRIPT%" --target-repo "%TARGET_REPO%" advance --initiative-id "%INITIATIVE_ID%" %DIRTY_FLAG%
echo.
pause
goto menu

:advance_dry
call :prompt_initiative
if not defined INITIATIVE_ID goto menu
python "%PING_PONG_SCRIPT%" --target-repo "%TARGET_REPO%" advance --initiative-id "%INITIATIVE_ID%" --dry-run
echo.
pause
goto menu

:approve_f2
call :prompt_initiative
if not defined INITIATIVE_ID goto menu
set "AUDITOR="
set /p AUDITOR=Motor auditor para F2 [codex]: 
if not defined AUDITOR set "AUDITOR=codex"
python "%PING_PONG_SCRIPT%" --target-repo "%TARGET_REPO%" approve-f2 --initiative-id "%INITIATIVE_ID%" --motor-auditor "%AUDITOR%"
echo.
pause
goto menu

:init_new
set "INITIATIVE_ID="
set /p INITIATIVE_ID=Nuevo initiative_id ^(YYYY-MM-DD_tema_corto^): 
if not defined INITIATIVE_ID goto menu
set "SUMMARY="
set /p SUMMARY=Resumen inicial opcional: 
set "MOTOR_ACTIVO="
set /p MOTOR_ACTIVO=Motor activo [claude]: 
if not defined MOTOR_ACTIVO set "MOTOR_ACTIVO=claude"
set "MOTOR_AUDITOR="
set /p MOTOR_AUDITOR=Motor auditor por defecto [codex]: 
if not defined MOTOR_AUDITOR set "MOTOR_AUDITOR=codex"
set "HANDOFF_FLAG="
choice /c SN /n /m "Crear handoff.md? [S/N]: "
if errorlevel 2 goto init_run
if errorlevel 1 set "HANDOFF_FLAG=--with-handoff"
:init_run
python "%PING_PONG_SCRIPT%" --target-repo "%TARGET_REPO%" init --initiative-id "%INITIATIVE_ID%" --motor-activo "%MOTOR_ACTIVO%" --motor-auditor "%MOTOR_AUDITOR%" --summary "%SUMMARY%" %HANDOFF_FLAG%
echo.
pause
goto menu

:tools
cls
echo Herramientas detectadas:
echo.
where claude
echo.
where codex
echo.
claude auth status
echo.
codex login status
echo.
pause
goto menu

:prompt_initiative
set "INITIATIVE_ID="
echo.
call :print_initiatives
echo.
set /p INITIATIVE_ID=Escribe initiative_id: 
if not defined INITIATIVE_ID (
    echo [INFO] No se selecciono iniciativa.
)
goto :eof

:print_initiatives
if not exist "%TARGET_REPO%\dev\records\initiatives" (
    echo [sin carpeta de iniciativas]
    goto :eof
)
set "HAS_ITEMS="
for /f "delims=" %%I in ('dir /b /ad "%TARGET_REPO%\dev\records\initiatives" 2^>nul') do (
    set "HAS_ITEMS=1"
    echo - %%I
)
if not defined HAS_ITEMS echo - [sin iniciativas]
goto :eof

:ensure_claude
where claude >nul 2>nul
if errorlevel 1 (
    echo [ERROR] No encuentro "claude" en PATH.
    echo         Abre una terminal donde funcione Claude Code antes de usar el launcher.
    pause
    exit /b 1
)
exit /b 0

:ensure_codex
where codex >nul 2>nul
if not errorlevel 1 exit /b 0

set "CODEX_DIR="
for /d %%D in ("%USERPROFILE%\.vscode\extensions\openai.chatgpt-*") do (
    if exist "%%~fD\bin\windows-x86_64\codex.exe" (
        set "CODEX_DIR=%%~fD\bin\windows-x86_64"
    )
)

if defined CODEX_DIR (
    set "PATH=%CODEX_DIR%;%PATH%"
    where codex >nul 2>nul
    if not errorlevel 1 exit /b 0
)

echo [ERROR] No encuentro "codex" en PATH ni en la extension de VS Code.
echo         Instala la extension de OpenAI o crea un alias valido para codex.
pause
exit /b 1
