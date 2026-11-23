@echo off
rem Levanta la interfaz de PrimerCraft Pro (HU-04) y abre el navegador.
rem   iniciar.bat           modo simulado (respuestas grabadas, no necesita internet)
rem   iniciar.bat real      consulta NCBI por internet
cd /d "%~dp0"

if not exist .venv (
    echo Preparando el entorno, solo la primera vez...
    python -m venv .venv
    .venv\Scripts\python -m pip install -q -r requirements.txt
)

if /i "%1"=="real" (set PRIMERCRAFT_NCBI=real) else (set PRIMERCRAFT_NCBI=simulado)

start "" http://127.0.0.1:8000
.venv\Scripts\python -m uvicorn src.interfaz.app:app
