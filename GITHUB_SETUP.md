# GitHub上传指南

## 准备工作

### 1. 检查敏感信息

确保以下文件不包含敏感信息：
- ✅ `backend/app/core/config.py` - 已脱敏数据库连接
- ✅ `.env` - 已在.gitignore中排除
- ✅ `*.log` - 已在.gitignore中排除
- ✅ 数据库备份文件 - 已在.gitignore中排除

### 2. 检查.gitignore配置

确保 `.gitignore` 包含以下内容：
- `.env` 和 `.env.*`
- `*.log` 和 `logs/`
- `*.sql` 和 `*.dump`
- `venv/` 和 `node_modules/`
- IDE配置文件（可选）

## 上传步骤

### 1. 初始化Git仓库（如果还没有）

```bash
# 初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/xiaoshi7915/on_campus_direct_recruitment.git
```

### 2. 添加文件到Git

```bash
# 添加所有文件（.gitignore会自动排除敏感文件）
git add .

# 检查要提交的文件（确保没有敏感信息）
git status
```

### 3. 提交代码

```bash
# 提交代码
git commit -m "Initial commit: 校园直聘平台 v1.0.0

- 完成核心功能开发
- 支持学生、企业、教师、管理员四种角色
- 实现在线聊天和系统消息功能
- 支持Docker一键部署
- 添加完整文档和部署脚本"
```

### 4. 推送到GitHub

```bash
# 推送到GitHub（首次推送）
git push -u origin main

# 如果main分支不存在，使用master
git push -u origin master

# 或者创建并切换到main分支
git checkout -b main
git push -u origin main
```

## 验证上传

访问 https://github.com/xiaoshi7915/on_campus_direct_recruitment 确认：
- ✅ 所有代码文件已上传
- ✅ 文档文件已上传（README.md, FEATURES.md, DEPLOYMENT.md等）
- ✅ 配置文件已上传（docker-compose.yml, Dockerfile等）
- ✅ `.env` 文件未上传（被.gitignore排除）
- ✅ 日志文件未上传
- ✅ 敏感信息已脱敏

## 后续更新

```bash
# 添加更改
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到GitHub
git push
```

## 注意事项

1. **永远不要提交敏感信息**：
   - 数据库密码
   - API密钥
   - OSS访问密钥
   - JWT密钥
   - 其他敏感配置

2. **定期更新文档**：
   - 功能更新后更新 FEATURES.md
   - 部署方式变更后更新 DEPLOYMENT.md
   - 重大更新后更新 README.md

3. **使用有意义的提交信息**：
   - 清晰描述更改内容
   - 遵循提交信息规范

4. **保护主分支**：
   - 建议在GitHub上设置分支保护规则
   - 使用Pull Request进行代码审查

## 分支管理建议

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发完成后合并到主分支
git checkout main
git merge feature/new-feature
git push
```

## 问题排查

如果遇到推送问题：

```bash
# 检查远程仓库配置
git remote -v

# 如果远程仓库URL错误，更新它
git remote set-url origin https://github.com/xiaoshi7915/on_campus_direct_recruitment.git

# 如果遇到冲突，先拉取最新代码
git pull origin main --rebase
```

