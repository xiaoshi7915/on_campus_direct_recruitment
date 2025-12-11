"""
Alembic环境配置文件
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入应用配置和模型
from app.core.config import settings
from app.core.database import Base
from app.models import *  # 导入所有模型以确保Alembic能够识别它们

# Alembic配置对象
config = context.config

# 从环境变量或配置文件读取数据库URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 如果配置了日志，则使用它
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据对象
target_metadata = Base.metadata

# 其他配置
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    在'offline'模式下运行迁移
    
    这将配置上下文，只使用URL而不是Engine，尽管Engine在这里也可以接受。
    通过跳过Engine创建，我们甚至不需要DBAPI可用。
    
    调用context.execute()来发出字符串到脚本输出。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    在'online'模式下运行迁移
    
    在这种情况下，我们需要创建一个Engine并将连接与上下文关联。
    """
    # 注意：这里使用同步引擎，因为Alembic不支持异步
    # 我们需要将异步URL转换为同步URL
    database_url = settings.DATABASE_URL
    if "mysql+aiomysql://" in database_url:
        database_url = database_url.replace("mysql+aiomysql://", "mysql+pymysql://")
    
    # 确保使用utf8mb4字符集
    if "?" not in database_url:
        database_url += "?charset=utf8mb4"
    elif "charset=" not in database_url:
        database_url += "&charset=utf8mb4"
    elif "charset=utf8" in database_url:
        database_url = database_url.replace("charset=utf8", "charset=utf8mb4")
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = database_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={
            "charset": "utf8mb4",
            "use_unicode": True,
        } if "pymysql" in database_url else {}
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

