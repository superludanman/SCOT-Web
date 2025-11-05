# SCOT-Web

An automated web page generation system based on structured thinking chain.

## 项目简介

SCOT-Web（Structured Chain-of-Thought Web）是一个基于结构化思维链的自动化网页生成系统。该系统旨在通过结构化逻辑自动生成网页内容，提升开发效率与内容组织能力。用户可以通过上传HTML文件或提供参考网站URL，系统将自动生成PRD文档、知识点图谱，并最终生成完整的网页。

## 功能特性

- **HTML文件上传与解析**：支持上传HTML文件并提取结构信息
- **PRD文档生成**：基于参考信息自动生成产品需求文档
- **知识点图谱提取**：从参考信息中提取结构化知识点
- **网页自动生成**：结合PRD文档和知识点图谱生成完整的网页
- **网页预览与下载**：提供生成网页的在线预览和文件下载功能

## 技术架构

### 前端
- Vue 3 + Composition API
- Axios for HTTP requests
- Vanilla CSS for styling

### 后端
- FastAPI (Python)
- OpenAI API integration
- Structured Chain-of-Thought processing

### 目录结构
```
SCOT-Web/
├── backend/              # 后端服务
│   ├── agents/           # AI代理模块
│   ├── api/              # API路由
│   ├── data/             # 数据存储目录
│   ├── executor/         # 任务执行器
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── frontend/             # 前端应用
│   ├── public/           # 静态资源
│   ├── src/              # 源代码
│   │   ├── api/          # API服务
│   │   ├── components/   # Vue组件
│   │   ├── styles/       # 样式文件
│   │   └── main.js       # 应用入口
│   └── index.html        # 主页面
└── README.md
```

## 环境要求

### 后端
- Python 3.8+
- pip (Python包管理器)

### 前端
- Node.js 14+
- npm 或 yarn

## 安装与部署

### 后端安装

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

5. 运行后端服务
```bash
python main.py
```

### 前端安装

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run dev
```

或者构建生产版本：
```bash
npm run build
```

## 使用说明

1. 启动后端服务（默认端口8000）
2. 启动前端开发服务器（默认端口3000）
3. 在浏览器中访问 http://localhost:3000
4. 使用流程：
   - 上传HTML文件或输入参考网站URL
   - 生成PRD文档
   - 提取知识点图谱
   - 执行网页生成任务
   - 预览和下载生成的网页

## API接口

### 上传相关
- `POST /api/upload/html` - 上传HTML文件
- `POST /api/upload/generate-prd` - 基于上传文件生成PRD
- `POST /api/upload/extract-knowledge` - 基于上传文件提取知识点

### PRD相关
- `POST /api/prd/generate` - 生成PRD文档
- `POST /api/prd/save` - 保存PRD文档
- `GET /api/prd` - 获取PRD列表
- `GET /api/prd/{id}` - 获取指定PRD
- `DELETE /api/prd/{id}` - 删除指定PRD
- `GET /api/prd/download/{id}` - 下载PRD文档

### 知识点相关
- `POST /api/knowledge/extract` - 提取知识点
- `POST /api/knowledge/save` - 保存知识点图谱
- `GET /api/knowledge` - 获取知识点图谱列表
- `GET /api/knowledge/{id}` - 获取指定知识点图谱
- `DELETE /api/knowledge/{id}` - 删除指定知识点图谱
- `GET /api/knowledge/download/{id}` - 下载知识点图谱

### 执行相关
- `POST /api/execute` - 执行网页生成任务
- `GET /api/execute/status/{task_id}` - 获取任务状态
- `GET /api/execute/download/{task_id}` - 下载生成的网页文件

### 预览相关
- `GET /api/preview/{task_id}` - 预览生成的网页
- `GET /api/preview/file/{task_id}/{file_path}` - 获取预览文件

## 开发指南

### 添加新功能

1. 在对应的router中添加新的API端点
2. 实现相应的业务逻辑
3. 在前端添加对应的组件和API调用

### 代码规范

- 后端遵循Python PEP8规范
- 前端遵循Vue.js风格指南
- API设计遵循RESTful原则

## 注意事项

1. 需要配置OpenAI API密钥才能正常使用AI功能
2. 生成的文件默认保存在`data`目录下
3. 确保后端服务运行时有读写文件的权限

## 许可证

[待定]

## 联系方式

[待定]