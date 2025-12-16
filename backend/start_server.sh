#!/bin/bash
# 启动后端服务脚本
cd "$(dirname "$0")"
export PYTHONPATH="$PWD"
python -m uvicorn app.main:app --reload --port 5011 --host 0.0.0.0


