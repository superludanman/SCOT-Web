from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from api.prd_router import prd_router
from api.knowledge_router import knowledge_router
from api.executor_router import executor_router
from api.logs_router import logs_router
from api.preview_router import preview_router
from api.upload_router import upload_router

app = FastAPI(
    title="结构化思维链网页智能生成与可视化系统（SCOT-Web）",
    description="基于结构化思维链（Structured Chain-of-Thought, SCOT）的网页自动生成与可视化平台",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]  # 允许前端访问Content-Disposition头
)

# 注册路由
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(prd_router, prefix="/api/prd", tags=["PRD"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(executor_router, prefix="/api/execute", tags=["Execute"])
app.include_router(preview_router, prefix="/api/preview", tags=["Preview"])
app.include_router(logs_router, prefix="/api/logs", tags=["Logs"])

@app.get("/")
async def root():
    return {"message": "欢迎使用结构化思维链网页智能生成与可视化系统（SCOT-Web）"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)