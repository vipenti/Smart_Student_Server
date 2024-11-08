@echo off

echo Starting Redis and Celery in Terminal 1...
start wsl -e bash -c "sudo service redis-server start && cd '$(wslpath '%cd%')' && celery -A tasks worker -l info"

timeout /t 2 >nul

echo Starting Flask in Terminal 2...
start wsl -e bash -c "export PYTHONPATH=\"${PYTHONPATH}:$(pwd)\" && export FLASK_APP=server.py && cd '$(wslpath '%cd%')' && flask run"
