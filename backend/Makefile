# Makefile for backend operations

.PHONY: help init-db test-db migrate upgrade downgrade run install

help:
	@echo "可用命令:"
	@echo "  make install      - 安装依赖"
	@echo "  make init-db      - 初始化数据库（创建表）"
	@echo "  make test-db      - 测试数据库连接"
	@echo "  make migrate      - 创建新的迁移脚本"
	@echo "  make upgrade      - 应用数据库迁移"
	@echo "  make downgrade    - 回退数据库迁移"
	@echo "  make run          - 启动开发服务器"

install:
	pip install -r requirements.txt

init-db:
	python scripts/init_db.py

test-db:
	python scripts/test_db.py

migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

run:
	uvicorn app.main:app --reload --port 5011



