"""
检查offers表是否存在及其结构
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


async def check_offers_table():
    """检查offers表是否存在及其结构"""
    async with engine.connect() as conn:
        # 检查表是否存在
        result = await conn.execute(text("SHOW TABLES LIKE 'offers'"))
        tables = result.fetchall()
        
        if not tables:
            print("❌ offers表不存在！")
            print("\n需要创建offers表。")
            return False
        
        print("✅ offers表存在")
        
        # 获取表结构
        result = await conn.execute(text("DESCRIBE offers"))
        columns = result.fetchall()
        
        print("\n表结构:")
        print(f"{'字段名':<20} {'类型':<30} {'允许NULL':<10} {'键':<10} {'默认值':<15}")
        print("-" * 85)
        for col in columns:
            field, type_, null, key, default, extra = col
            print(f"{field:<20} {type_:<30} {null:<10} {key:<10} {str(default):<15}")
        
        # 检查关键字段
        field_names = [col[0] for col in columns]
        required_fields = ['id', 'application_id', 'enterprise_id', 'student_id', 'job_title', 'content', 'status', 'created_at', 'updated_at']
        
        print("\n关键字段检查:")
        missing_fields = []
        for field in required_fields:
            if field in field_names:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ {field} - 缺失")
                missing_fields.append(field)
        
        if missing_fields:
            print(f"\n⚠️ 缺少字段: {', '.join(missing_fields)}")
            return False
        
        return True


if __name__ == "__main__":
    asyncio.run(check_offers_table())


