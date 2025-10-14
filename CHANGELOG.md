# 更新日志

所有项目重要变更都会记录在此文件中。

## [0.1.1] - 2025-10-14

### 文档
- 📝 新增Git开发工作流程最佳实践到CLAUDE.md
- 🔧 添加Git Flow和GitHub Flow分支策略说明
- 📋 完善提交规范和核心开发原则
- 📖 补充日常Git操作指南和最佳实践

## [0.1.0] - 2025-10-14

### 新增
- 🎉 初始化Tadmin全栈管理系统
- ✨ 完整的用户认证和JWT权限管理系统
- 🚀 基于FastAPI + Vue3 + TypeScript的现代化架构
- 🎨 Element Plus UI组件库 + Tailwind CSS样式系统
- 📱 响应式设计和主题切换功能
- 🌐 国际化支持（中文/英文）
- 🔧 完整的开发工具链和脚本配置
- 🧪 Playwright自动化测试集成
- 📊 完整的项目文档和开发指南

### 修复
- 🔐 修复token刷新参数名不匹配问题（refresh_token vs refreshToken）
- 🎯 解决UI组件视口定位问题
- ⚡ 优化前后端数据交互流程

### 技术栈
- **后端**: FastAPI, SQLModel, JWT, Alembic, uv
- **前端**: Vue 3, TypeScript, Element Plus, Vite, pnpm
- **数据库**: SQLite (开发), PostgreSQL (生产)
- **测试**: Playwright E2E测试
- **工具**: ESLint, Prettier, Stylelint, Ruff

### 默认配置
- **管理员账号**: admin@example.com / admin123
- **前端地址**: http://localhost:8848
- **后端地址**: http://localhost:8000
- **API文档**: http://localhost:8000/docs