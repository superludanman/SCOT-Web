from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload_router import upload_router
from api.prd_router import prd_router
from api.knowledge_router import knowledge_router
from api.executor_router import executor_router
from api.preview_router import preview_router
from api.logs_router import logs_router
from api.learning_router import learning_router
from api.test_router import test_router  # 添加这一行
import os

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]  # 暴露Content-Disposition头部，用于文件下载
)

# 注册路由
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(prd_router, prefix="/api/prd", tags=["PRD"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(executor_router, prefix="/api/execute", tags=["Executor"])
app.include_router(preview_router, prefix="/api/preview", tags=["Preview"])
app.include_router(logs_router, prefix="/api/logs", tags=["Logs"])
app.include_router(learning_router, prefix="/api/learning", tags=["Learning"])
app.include_router(test_router, prefix="/api/test", tags=["Test"])  # 添加这一行

@app.get("/")
async def root():
    return {"message": "SCOT-Web Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)