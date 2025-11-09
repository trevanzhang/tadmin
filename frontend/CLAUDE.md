# Frontend 模块文档

[根目录](../../CLAUDE.md) > **frontend**

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建frontend模块文档
- 分析Vue3组件架构和路由系统
- 识别状态管理和API调用机制

## 模块职责

Frontend模块负责构建现代化的Web管理界面，基于Vue 3 + TypeScript + Element Plus技术栈。提供响应式布局、权限管理、路由守卫等完整的前端功能，并集成了Playwright E2E测试框架。

## 入口与启动

### 应用入口
- **主文件**: `src/main.ts`
- **根组件**: `src/App.vue`
- **启动命令**: `pnpm dev`
- **开发服务器**: `http://localhost:8848`
- **构建命令**: `pnpm build`

### 启动流程
1. 加载样式和字体图标
2. 注册全局组件和指令
3. 配置路由和状态管理
4. 初始化UI组件库
5. 挂载Vue应用

## 对外接口

### API服务层 (`src/api/`)
- **用户API**: `src/api/user.ts`
  - `getLogin(data)` - 用户登录
  - `refreshTokenApi(data)` - 刷新令牌

### 路由接口 (`src/router/`)
- **动态路由**: 支持基于权限的路由生成
- **路由守卫**: 自动进行身份验证检查
- **面包屑导航**: 自动生成页面层级

### HTTP客户端 (`src/utils/http/`)
- **请求拦截器**: 自动添加认证头
- **响应拦截器**: 统一错误处理
- **令牌刷新**: 自动处理过期令牌

## 关键依赖与配置

### 核心依赖
```json
{
  "vue": "^3.5.18",
  "vue-router": "^4.5.1",
  "pinia": "^3.0.3",
  "element-plus": "^2.10.4",
  "typescript": "^5.8.3",
  "vite": "^7.0.6"
}
```

### 开发依赖
```json
{
  "@playwright/test": "^1.56.0",
  "eslint": "^9.32.0",
  "prettier": "^3.6.2",
  "tailwindcss": "^4.1.11"
}
```

### 构建配置
- **Vite配置**: `vite.config.ts`
- **TypeScript配置**: `tsconfig.json`
- **ESLint配置**: `eslint.config.js`
- **样式配置**: `tailwindcss`

## 组件架构

### 布局系统 (`src/layout/`)
- **主布局**: `src/layout/index.vue`
- **导航栏**: `components/lay-navbar/`
- **侧边栏**: `components/lay-sidebar/`
- **内容区**: `components/lay-content/`
- **标签页**: `components/lay-tag/`
- **设置面板**: `components/lay-setting/`

### 公共组件 (`src/components/`)
- **图标组件**: `ReIcon/` - 支持在线/离线图标
- **对话框组件**: `ReDialog/` - 统一弹窗管理
- **权限组件**: `ReAuth/`, `RePerms/` - 按钮级权限控制
- **表格组件**: 集成Pure Table
- **文本组件**: `ReText/`

### 页面组件 (`src/views/`)
- **登录页**: `views/login/`
- **欢迎页**: `views/welcome/`
- **错误页**: `views/error/` (403, 404, 500)
- **权限页**: `views/permission/`

## 状态管理

### Pinia Store结构 (`src/store/modules/`)
- **用户状态**: `user.ts` - 用户信息、登录状态
- **应用设置**: `app.ts` - 侧边栏、设备类型
- **系统设置**: `settings.ts` - 主题、布局配置
- **权限管理**: `permission.ts` - 路由权限
- **多标签页**: `multiTags.ts` - 标签页管理
- **主题设置**: `epTheme.ts` - Element Plus主题

### 用户状态管理示例
```typescript
export const useUserStore = defineStore("pure-user", {
  state: (): userType => ({
    avatar: "",
    username: "",
    nickname: "",
    roles: [],
    permissions: []
  }),
  actions: {
    async loginByUsername(data) { /* 登录逻辑 */ },
    logOut() { /* 登出逻辑 */ },
    async handRefreshToken(data) { /* 刷新令牌 */ }
  }
});
```

## 路由系统

### 路由配置 (`src/router/`)
- **静态路由**: `modules/` 目录下的路由模块
- **动态路由**: 基于用户权限动态生成
- **路由守卫**: 身份验证和权限检查
- **面包屑**: 自动生成页面层级导航

### 路由特性
- **多级菜单**: 支持无限层级路由
- **权限控制**: 页面级和按钮级权限
- **缓存机制**: keep-alive页面缓存
- **标签页**: 多标签页导航

## 测试与质量

### E2E测试 (Playwright)
- **配置文件**: `playwright.config.ts`
- **测试目录**: `tests/`
- **基础URL**: `http://localhost:8848`
- **浏览器支持**: Chrome, Firefox, Safari

### 测试命令
```bash
pnpm test:e2e              # 运行E2E测试
pnpm test:e2e:ui           # UI模式测试
pnpm test:e2e:debug        # 调试模式测试
pnpm test:e2e:codegen      # 代码生成器
```

### 代码质量工具
- **ESLint**: 代码检查
- **Prettier**: 代码格式化
- **Stylelint**: 样式检查
- **TypeScript**: 类型检查

### 质量命令
```bash
pnpm lint                  # 代码检查和格式化
pnpm typecheck             # TypeScript类型检查
```

## 工具与插件

### 构建工具 (`build/`)
- **插件配置**: `build/plugins.ts`
- **优化配置**: `build/optimize.ts`
- **压缩配置**: `build/compress.ts`
- **CDN配置**: `build/cdn.ts`

### 工具函数 (`src/utils/`)
- **HTTP工具**: `http/` - 请求封装
- **认证工具**: `auth.ts` - 令牌管理
- **存储工具**: `localforage/` - 本地存储
- **响应式工具**: `responsive.ts` - 设备检测
- **工具类**: `tree.ts`, `message.ts`, `progress.ts` 等

### 自定义指令 (`src/directives/`)
- **长按指令**: `longpress/`
- **复制指令**: `copy/`
- **权限指令**: `auth/`, `perms/`
- **波纹指令**: `ripple/`
- **优化指令**: `optimize/`

## 主题与样式

### 样式系统
- **CSS框架**: Tailwind CSS 4.1+
- **UI组件**: Element Plus 2.10+
- **主题切换**: 支持亮色/暗色主题
- **响应式**: 移动端适配

### 样式文件结构
```
src/style/
├── reset.scss       # 样式重置
├── index.scss       # 全局样式
└── tailwind.css     # Tailwind样式
```

## 国际化支持

### i18n配置 (`src/plugins/i18n.ts`)
- **语言切换**: 支持多语言切换
- **文本翻译**: 使用vue-i18n
- **日期格式化**: 本地化日期时间
- **数字格式化**: 本地化数字显示

## 常见问题 (FAQ)

### Q: 如何添加新的页面？
A: 在`src/views/`目录下创建新组件，然后在`src/router/modules/`中添加路由配置。

### Q: 如何实现权限控制？
A: 使用路由守卫和权限指令，结合用户的roles和permissions进行控制。

### Q: 如何自定义主题？
A: 修改`src/layout/hooks/useDataThemeChange.ts`中的主题配置，或使用设置面板。

### Q: 如何添加新的API接口？
A: 在`src/api/`目录下创建新的API文件，使用HTTP工具函数进行请求封装。

### Q: 如何进行E2E测试？
A: 使用Playwright，参考`tests/`目录下的示例，可以通过UI模式进行调试。

## 相关文件清单

### 核心文件
- `src/main.ts` - 应用入口
- `src/App.vue` - 根组件
- `src/layout/index.vue` - 主布局

### 配置文件
- `package.json` - 项目配置
- `vite.config.ts` - 构建配置
- `tsconfig.json` - TypeScript配置
- `playwright.config.ts` - E2E测试配置

### 核心模块
- `src/router/` - 路由管理
- `src/store/` - 状态管理
- `src/api/` - API接口
- `src/utils/` - 工具函数
- `src/components/` - 公共组件
- `src/views/` - 页面组件

### 样式文件
- `src/style/` - 样式文件
- `tailwind.config.js` - Tailwind配置

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建frontend模块文档
- 分析Vue3组件架构和路由系统
- 识别状态管理和API调用机制