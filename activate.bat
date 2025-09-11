@echo off
echo Activating TTS virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo Available scripts:
echo - python tts.py          (Google TTS - requires internet)
echo - python tts_offline.py  (Offline TTS - no internet required)
echo - python test_env.py     (Test environment)
echo.
