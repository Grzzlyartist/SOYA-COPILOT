@echo off
echo Cleaning up Python cache files...
echo.

REM Remove all __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Remove all .pyc files
del /s /q *.pyc 2>nul

REM Remove all .pyo files
del /s /q *.pyo 2>nul

echo.
echo ✅ Cache cleanup complete!
pause
