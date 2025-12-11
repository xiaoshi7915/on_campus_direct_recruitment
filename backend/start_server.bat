@echo off
REM 启动后端服务脚本
cd /d %~dp0
set PYTHONPATH=%CD%
python -m uvicorn app.main:app --reload --port 5001 --host 0.0.0.0
pause


