#!/bin/bash
# 运行修复接口的测试脚本

echo "=========================================="
echo "开始测试修复后的接口"
echo "=========================================="

# 进入backend目录
cd "$(dirname "$0")/.." || exit 1

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../py312" ]; then
    source ../py312/bin/activate
fi

# 运行测试
echo ""
echo "运行测试: test_fixed_interfaces.py"
echo "----------------------------------------"
pytest tests/test_fixed_interfaces.py -v --tb=short --color=yes

# 检查测试结果
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 所有测试通过！"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ 部分测试失败，请检查错误信息"
    echo "=========================================="
    exit 1
fi

