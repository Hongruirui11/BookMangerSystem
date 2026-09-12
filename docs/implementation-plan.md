# 图书管理系统实现计划

## Phase 0：文档发现与约束

已核对的官方文档：

- FastAPI 静态文件：<https://fastapi.tiangolo.com/tutorial/static-files/>；使用 `fastapi.staticfiles.StaticFiles` 并通过 `app.mount()` 挂载，挂载应用独立于 `APIRouter`。
- FastAPI CORS：<https://fastapi.tiangolo.com/tutorial/cors/>；使用 `CORSMiddleware` 配置本地前端开发源。
- Tortoise FastAPI 集成：<https://tortoise.github.io/contrib/fastapi.html>；使用 `tortoise.contrib.fastapi.RegisterTortoise` 管理应用生命周期，配置 `connections` 和 `apps`。
- Tortoise 数据库：<https://tortoise.github.io/databases.html>；MySQL URL 形如 `mysql://user:password@host:3306/database`，支持 `asyncmy` 或 `aiomysql` 驱动。
- Tortoise 入门：<https://tortoise.github.io/getting_started.html>；MySQL 安装额外依赖，开发环境可使用 `generate_schemas` 创建空库表。
- Vue 快速开始：<https://vuejs.org/guide/quick-start>；使用 `npm create vue@latest` 创建 Vite-powered Vue 3 项目。

约束：不凭空引入未记录的 ORM 初始化 API；不把真实 `.env`、密码、`node_modules` 或构建产物提交到 Git；开发阶段可以生成 schema，README 中明确这不是生产迁移方案。

## Phase 1：项目骨架和开发环境

实现：

- 创建 `backend/`、`frontend/`、`docs/` 的教学目录。
- 后端建立虚拟环境、依赖文件、`.env.example` 和 FastAPI 最小入口。
- 前端使用 `npm create vue@latest` 生成 Vue 3 + Vite 基础项目。
- 增加根目录 `.gitignore`，覆盖 `.env`、虚拟环境、`node_modules`、构建目录和 IDE 文件。

参考：Vue 官方 Quick Start；Tortoise Getting Started 的 MySQL extra dependency 表。

验证：后端启动后访问 `/docs`；前端启动后显示默认页面；`git status` 不显示被忽略的依赖和环境文件。

防错：不使用 Vue CLI；不把 MySQL 密码写入源码；不在后端依赖中混用不需要的同步 MySQL 客户端。

## Phase 2：FastAPI 路由分发与基础示例

实现：

- 新建 `api/routes/books.py`，使用 `APIRouter` 定义图书相关路由。
- 在 `main.py` 中使用 `app.include_router()` 注册路由，并设置 API 前缀和标签。
- 添加健康检查接口和 Request 示例接口，读取请求方法、URL、客户端信息或请求头。
- 配置 `CORSMiddleware`，只允许本地 Vite 地址。

参考：FastAPI CORS 官方文档；FastAPI 路由器的官方教程（实现时补充对应官方链接和版本检查）。

验证：OpenAPI `/docs` 能显示分组路由；健康检查返回 JSON；Request 示例能返回请求上下文；跨域预检请求包含正确响应头。

防错：不把所有路由写进 `main.py`；不把 Request 对象当作 Pydantic 请求体模型；路由固定路径 `/search` 必须注册在动态路径 `/{book_id}` 之前。

## Phase 3：Tortoise-ORM 与 MySQL

实现：

- 创建 `models/book.py`，定义 `Book` 模型和字段约束。
- 创建数据库配置模块，从环境变量读取 MySQL 连接信息。
- 使用 `RegisterTortoise` 接入 FastAPI 生命周期，注册模型模块。
- 提供开发环境初始化说明和可选 schema 生成方式。

参考：Tortoise FastAPI integration 的 `RegisterTortoise`；Tortoise Databases 的 MySQL URL、驱动和配置说明。

验证：连接真实 MySQL 数据库成功；启动时表结构可用；模型可通过 ORM 创建并查询一条记录；错误连接能产生清晰日志。

防错：不提交真实连接串；不在生产语义下依赖 `generate_schemas`；密码含特殊字符时使用 URL 编码或字典配置。

## Phase 4：图书 CRUD API

实现：

- 创建 Pydantic 的创建、更新、响应模型。
- 实现列表、搜索、详情、新增、编辑、删除接口。
- 将数据库操作保持在路由可读的简单边界内；对不存在的图书返回 404。
- 统一返回字段和错误结构，设置合适 HTTP 状态码。

参考：FastAPI 官方请求体、响应模型和错误处理教程；Tortoise 官方 FastAPI example 与模型查询文档（实现前核对最新签名）。

验证：使用 FastAPI TestClient 或 HTTP 请求覆盖成功和失败路径；检查 422 校验错误、404、创建 201 和删除 204/明确 JSON 响应；确认搜索不影响列表接口。

防错：不直接把 ORM 实例未经序列化返回；不在查询字符串中拼接 SQL；更新时明确允许修改的字段。

## Phase 5：静态文件、模板和教学示例

实现：

- 添加 `backend/static/` 和 `backend/templates/`。
- 用 `StaticFiles` 挂载 `/static`。
- 用 Jinja2 模板渲染 `/` 或 `/about` 教学页，并显式使用 `Request`。
- 让该页说明 API 地址和项目知识点，与 Vue 业务页面保持独立。

参考：FastAPI Static Files 官方文档；FastAPI Templates 官方文档（实现前核对 `TemplateResponse` 当前签名）。

验证：浏览器访问模板页成功；模板引用的静态 CSS/图片可访问；API 路由不被静态挂载遮蔽。

防错：不使用模板页替代 Vue 主业务页面；不把静态目录误挂到 API 前缀；不依赖旧版模板响应参数顺序。

## Phase 6：Vue 图书管理界面

实现：

- 建立 API 封装模块。
- 创建图书列表、搜索、详情/编辑表单和删除确认交互。
- 管理加载、成功、空列表和错误状态。
- 使用环境变量配置 API 基础地址；保持组件职责清晰。

参考：Vue Quick Start 和官方 Composition API 文档；实现时只引入必要依赖，不额外加入状态管理库。

验证：前端能完成完整 CRUD 联调；搜索结果与 API 一致；刷新后数据来自 MySQL；错误响应能显示给用户。

防错：不把后端数据库逻辑复制到前端；不把密钥放入 `VITE_` 变量；不让组件散落重复的 fetch 逻辑。

## Phase 7：GitHub 远程仓库与交付

实现：

- 分阶段提交，提交信息保持清晰。
- 检查工作区没有密钥、依赖目录和构建产物。
- 创建新的 GitHub 仓库，配置 `origin`，推送 `main` 分支。
- 完善 README：环境要求、MySQL 建库、环境变量、启动命令、接口列表、知识点文件索引。

验证：`git log` 可追踪阶段提交；`git remote -v` 指向用户的新仓库；GitHub 上能看到完整代码；按 README 可从空环境启动并完成 CRUD。

防错：创建 GitHub 仓库前确认仓库名称和可见性；不使用强制推送覆盖远程历史；不在命令行或提交中暴露密码。

## 最终验证

- 后端静态检查/测试通过。
- 前端构建通过。
- MySQL 连接、建表和 CRUD 通过。
- `/docs`、Request 示例、模板页、静态文件和 Vue 页面均可访问。
- 逐项对照设计文档中的知识点和范围，确认无额外复杂功能混入。
