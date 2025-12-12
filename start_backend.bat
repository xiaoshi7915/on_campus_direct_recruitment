@echo off
REM 启动后端服务
echo 正在启动后端服务...
cd backend
set PYTHONPATH=%CD%
python -m uvicorn app.main:app --reload --port 5011 --host 0.0.0.0


