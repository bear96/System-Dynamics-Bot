@echo off
setlocal

:check_admin
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :is_admin
) else (
    goto :request_admin
)

:is_admin
where dot >nul 2>&1
if %errorLevel% == 0 (
    echo Found existing Graphviz installation. Continuing to pygraphviz installation.
    goto :install_pygraphviz
) else (
    echo Detected OS Windows
    echo Installing Graphviz2.6...
    goto :install_graphviz
)

:request_admin
powershell -Command "Start-Process '%~f0' -Verb runAs"
exit /b

:install_graphviz
start /wait "" "%~dp0stable_windows_10_cmake_Release_x64_graphviz-install-2.46.0-win64.exe"
if %errorLevel% neq 0 (
    echo Failed to run Graphviz installer. Exit code: %errorLevel%
    pause
    exit /b %errorLevel%
)

:find_graphviz
echo Searching for Graphviz installation...
for /r "C:\" %%i in (dot.exe) do (
    set "GRAPHVIZ_BIN=%%~dpi"
    goto :graphviz_found
)

:graphviz_found
if defined GRAPHVIZ_BIN (
    echo Graphviz found at %GRAPHVIZ_BIN%
    echo Please add %GRAPHVIZ_BIN% to your PATH environment variable.
    echo The script will close in 15 seconds. Please restart the script after updating the PATH.
    timeout /t 15
    exit /b
) else (
    echo Graphviz installation could not be found. Please ensure it is installed correctly.
    pause
    exit /b
)

:check_graphviz
where dot >nul 2>&1
if %errorLevel% neq 0 (
    echo Waiting for Graphviz installation to complete. If installation is complete and you're still seeing this message, that means you need to add Graphviz to PATH.
    timeout /t 15
    goto :check_graphviz
)

echo Graphviz installation completed successfully.
goto :install_pygraphviz

:install_pygraphviz
echo Installing pygraphviz...
pip install --use-pep517 --config-setting="--global-option=build_ext" --config-setting="--global-option=-IC:\Program Files\Graphviz\include" --config-setting="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz

if %errorLevel% neq 0 (
    echo Something unexpected occurred. Either Graphviz was not installed correctly, or there is a version conflict. Just give up.
    pause
)

pip install -r "%~dp0requirements.txt"

endlocal
pause
exit /b 0
