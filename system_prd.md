非常好 ✅
以下是为你的项目生成的 **Markdown 版 PRD 文档**（命名建议：`/docs/system_prd.md`）。
它可直接提交给 AI 编程工具、代码生成器或版本控制系统（如 GitHub）。
结构化格式清晰、提示信息完整、兼容多模型解析。

---

```markdown
# 🧠 《结构化思维链网页智能生成与可视化系统（SCOT-Web）》PRD 文档

---

## 一、系统概述

本系统旨在构建一个基于 **结构化思维链（Structured Chain-of-Thought, SCOT）** 的网页自动生成与可视化平台。  
通过结合 **Slow-Fast 分层模型架构**，系统实现从用户模糊需求 → 产品需求文档（PRD） → 任务拆解（Task Tree） → 自动代码生成 → 网页可视化预览 的全流程。

---

## 二、系统目标

1. 用户可以上传网页文件或输入网页链接作为参考；
2. 系统自动提取网页结构与语义信息，生成对应的 PRD；
3. 系统根据 PRD 进行任务拆解，形成任务树；
4. 系统根据任务树逐步生成完整网页项目（HTML / CSS / JS）；
5. 前端可实时查看生成结果与知识图谱；
6. 提供日志记录、任务管理与文件可视化功能。

---

## 三、系统架构

### 3.1 技术选型

| 模块 | 技术栈 |
|------|---------|
| 前端 | Vue3 + Vite + Element Plus + Axios |
| 后端 | FastAPI + Python 3.10+ |
| 存储 | JSON 文件（可扩展 SQLite） |
| AI 接口 | OpenAI GPT 系列（经统一封装） |

---

## 四、项目结构

```

scot-web/
├── backend/
│   ├── main.py                     # FastAPI 主入口
│   ├── api/
│   │   ├── upload_router.py        # 上传与网页结构提取
│   │   ├── prd_router.py           # PRD 文档生成与管理
│   │   ├── knowledge_router.py     # 知识图谱展示
│   │   ├── executor_router.py      # 任务执行与网页生成
│   │   ├── preview_router.py       # 前端网页预览接口
│   │   └── logs_router.py          # 日志查询
│   ├── agents/
│   │   ├── slow_mind.py            # 模糊需求 → PRD
│   │   └── fast_mind.py            # PRD → 任务拆解
│   ├── executor/
│   │   ├── task_executor.py        # AI 执行任务生成网页
│   │   └── execution_context.py    # 模型配置与上下文
│   ├── planner/
│   │   └── task_splitter.py        # 构建任务树与依赖关系
│   ├── utils/
│   │   ├── file_manager.py         # 文件操作工具
│   │   ├── config_loader.py        # 环境变量读取
│   │   └── logger.py               # 日志管理
│   └── data/
│       ├── prd/
│       ├── knowledge/
│       ├── tasks/
│       ├── results/
│       └── logs/
│
└── frontend/
├── src/
│   ├── App.vue
│   ├── main.js
│   ├── api/
│   │   ├── index.js
│   │   └── service.js
│   ├── components/
│   │   ├── UploadPanel.vue
│   │   ├── PRDPanel.vue
│   │   ├── KnowledgeGraph.vue
│   │   ├── GeneratePanel.vue
│   │   └── PreviewPane.vue
│   ├── pages/
│   │   ├── Dashboard.vue
│   │   └── TaskHistory.vue
│   └── router/
│       └── index.js
└── public/index.html

````

---

## 五、后端功能说明

### 5.1 `main.py`
- 创建 FastAPI 应用；
- 挂载各功能模块；
- 启用跨域访问；
- `/health` 路由返回运行状态。

---

### 5.2 `upload_router.py`
上传 HTML 文件或输入 URL，提取网页结构。

**接口示例：**
```python
POST /api/upload/html
参数：
- file: HTML 文件
- url: 可选网页链接

返回：
{
  "title": "页面标题",
  "structure": [...],
  "text_blocks": [...]
}
````

---

### 5.3 `prd_router.py`

基于上传网页结构生成 PRD。

```python
POST /api/prd/generate
参数：
- reference_html: 提取的网页结构
- user_input: 用户需求描述

返回：
{
  "prd_text": "...PRD 内容...",
  "status": "success"
}
```

---

### 5.4 `executor_router.py`

根据任务执行自动生成网页。

```python
POST /api/execute
参数：
- task_id: 任务 ID
- user_note: 用户补充说明

返回：
{
  "status": "success",
  "files": ["index.html", "style.css"],
  "preview_url": "/api/preview/1"
}
```

---

### 5.5 `preview_router.py`

网页预览接口。

```python
GET /api/preview/{task_id}
返回：
HTML 文件内容
```

---

### 5.6 `logs_router.py`

日志查询接口。

```python
GET /api/logs
返回：
{
  "task_id": "1",
  "timestamp": "...",
  "files": [...],
  "status": "completed"
}
```

---

## 六、前端模块功能

| 组件名                    | 功能                       |
| ---------------------- | ------------------------ |
| **UploadPanel.vue**    | 上传 HTML 文件或输入 URL，展示解析结构 |
| **PRDPanel.vue**       | 展示、编辑、保存生成的 PRD          |
| **GeneratePanel.vue**  | 输入说明，触发网页自动生成            |
| **PreviewPane.vue**    | 网页实时预览（iframe）           |
| **KnowledgeGraph.vue** | 展示任务依赖关系与结构              |
| **Dashboard.vue**      | 系统主页面，整合功能模块             |
| **TaskHistory.vue**    | 查看任务执行历史与日志              |

---

## 七、环境配置

### 后端依赖

```
fastapi
uvicorn
openai
python-multipart
aiofiles
pydantic
requests
```

### 前端依赖

```
vue
vite
element-plus
axios
cytoscape
```

---

## 八、运行说明

* 启动后端：

  ```bash
  uvicorn backend.main:app --reload --port 8000
  ```

* 启动前端：

  ```bash
  npm run dev
  ```

* 前端访问地址：

  ```
  http://localhost:5173
  ```

* 后端接口地址：

  ```
  http://localhost:8000
  ```

---

## 九、系统输出要求

1. 后端代码需带类型注解、函数文档、返回示例；
2. 前端组件需包含基本 UI 与交互逻辑；
3. 所有模块文件按功能归类；
4. 确保前后端接口联通、可运行；
5. 所有生成的文件可通过 Vite + FastAPI 联调。

---

## 十、AI 执行提示（供 AI 编程工具使用）

> 请根据以上 PRD：
>
> 1. 生成完整项目文件结构；
> 2. 自动创建必要文件；
> 3. 为每个后端接口生成 FastAPI 函数骨架；
> 4. 为每个前端组件生成 Vue 模板；
> 5. 生成 requirements.txt 与 package.json；
> 6. 输出后端与前端启动命令；
> 7. 不要输出解释文字，只输出可运行代码。

---

### ✅ 输出格式要求：

* 每个文件内容用以下格式包裹：

  ````
  ```python filename=backend/api/prd_router.py
  # 代码内容
  ````

  ```vue filename=frontend/src/components/UploadPanel.vue
  <!-- Vue 组件 -->
  ```
* 所有路径正确、文件结构清晰；
* 保证生成结果可以直接 `npm run dev` + `uvicorn main:app` 跑通。

---

📁 **推荐保存路径：**

```
/docs/system_prd.md
```

📅 **版本：** v1.0.0
🧱 **维护者：** 卢毅恒

```

---

是否希望我 **接着帮你生成 `/docs/system_prd.json` 版本**？  
（可供自动化工具或 RAG 系统直接读取使用）
```
